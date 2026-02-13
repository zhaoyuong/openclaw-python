"""Bash execution tool with exec security configuration"""
from __future__ import annotations


import asyncio
import logging
import os
import shlex
from pathlib import Path
from typing import Any

from .base import AgentTool, ToolResult

logger = logging.getLogger(__name__)


class BashTool(AgentTool):
    """Execute bash commands with configurable security modes and approval workflow"""

    def __init__(
        self,
        exec_config: dict | None = None,
        workspace_dir: Path | None = None,
        approval_manager: Any | None = None
    ):
        """
        Initialize BashTool with exec configuration
        
        Args:
            exec_config: Exec configuration dict (host, security, ask, safe_bins, etc.)
            workspace_dir: Default workspace directory for commands
            approval_manager: ExecApprovalManager for command approval workflow
        """
        super().__init__()
        self.name = "bash"
        self.description = (
            "Execute bash commands in a shell with FULL access. "
            "NO sandbox restrictions. You can run ANY command, install packages, execute Python scripts. "
            "All system tools and libraries (including python-pptx) are available. "
            "Use for system operations, running scripts, file operations, package installations, etc."
        )
        
        # Load exec config
        self.exec_config = exec_config or {}
        self.security_mode = self.exec_config.get("security", "full")
        self.ask_mode = self.exec_config.get("ask", "off")  # off | on-miss | always
        self.safe_bins = set(self.exec_config.get("safe_bins", []))
        self.path_prepend = self.exec_config.get("path_prepend", [])
        self.timeout_sec = self.exec_config.get("timeout_sec", 120)
        self.workspace_dir = workspace_dir
        self.approval_manager = approval_manager

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "The bash command to execute"},
                "working_directory": {
                    "type": "string",
                    "description": "Optional working directory for the command",
                },
            },
            "required": ["command"],
        }

    def _check_security(self, command: str) -> tuple[bool, str | None]:
        """
        Check if command is allowed based on security mode
        
        Returns:
            (allowed, reason_if_denied)
        """
        if self.security_mode == "deny":
            return False, "Exec security mode is 'deny' - all commands blocked"
        
        if self.security_mode == "full":
            return True, None
        
        # allowlist mode - check if command uses safe binaries
        if self.security_mode == "allowlist":
            # Extract the first command (before pipes, &&, ||, etc.)
            try:
                parts = shlex.split(command.split("|")[0].split("&&")[0].split("||")[0].split(";")[0].strip())
                if not parts:
                    return False, "Empty command"
                
                binary = Path(parts[0]).name
                
                # Check if binary is in safe_bins
                if binary in self.safe_bins:
                    return True, None
                
                # Also check without extension (for .exe on Windows)
                binary_no_ext = binary.rsplit(".", 1)[0] if "." in binary else binary
                if binary_no_ext in self.safe_bins:
                    return True, None
                
                return False, f"Binary '{binary}' not in safe_bins allowlist. Security mode is 'allowlist'."
                
            except Exception as e:
                logger.warning(f"Failed to parse command for allowlist check: {e}")
                return False, f"Failed to parse command: {e}"
        
        return False, f"Unknown security mode: {self.security_mode}"

    def _build_env(self, base_env: dict[str, str] | None = None) -> dict[str, str]:
        """Build environment with PATH prepend"""
        env = base_env.copy() if base_env else os.environ.copy()
        
        if self.path_prepend:
            current_path = env.get("PATH", "")
            prepend_path = os.pathsep.join(self.path_prepend)
            env["PATH"] = f"{prepend_path}{os.pathsep}{current_path}" if current_path else prepend_path
        
        return env

    def _should_request_approval(self, command: str, security_passed: bool) -> bool:
        """Determine if approval is needed based on ask_mode"""
        if self.ask_mode == "off":
            return False
        
        if self.ask_mode == "always":
            return True
        
        if self.ask_mode == "on-miss":
            # Request approval if security check would block it
            return not security_passed
        
        return False
    
    async def execute(self, params: dict[str, Any]) -> ToolResult:
        """Execute bash command with security checks and approval workflow"""
        command = params.get("command", "")
        working_dir = params.get("working_directory")

        if not command:
            return ToolResult(success=False, content="", error="No command provided")

        # Security check
        allowed, reason = self._check_security(command)
        
        # Check if approval is needed
        needs_approval = self._should_request_approval(command, allowed)
        
        if needs_approval and self.approval_manager:
            logger.info(f"Requesting approval for command: {command[:100]}")
            
            # Request approval
            approval_id = self.approval_manager.request_approval(
                command=command,
                context={
                    "security_mode": self.security_mode,
                    "ask_mode": self.ask_mode,
                    "security_passed": allowed,
                    "working_dir": working_dir
                }
            )
            
            # Wait for approval (with timeout)
            try:
                approved = await asyncio.wait_for(
                    self._wait_for_approval(approval_id),
                    timeout=300  # 5 minutes timeout
                )
                
                if not approved:
                    logger.warning(f"Command rejected by user: {command[:100]}")
                    return ToolResult(
                        success=False,
                        content="",
                        error="Command execution rejected by user",
                        metadata={"approval_id": approval_id, "approved": False}
                    )
                
                logger.info(f"Command approved: {command[:100]}")
                # Override security check if approved
                allowed = True
                
            except asyncio.TimeoutError:
                logger.warning(f"Approval timeout for command: {command[:100]}")
                return ToolResult(
                    success=False,
                    content="",
                    error="Approval request timed out (5 minutes)",
                    metadata={"approval_id": approval_id, "timeout": True}
                )
        
        # Check security (unless approved)
        if not allowed:
            logger.warning(f"Command blocked by security policy: {command[:100]}")
            return ToolResult(
                success=False,
                content="",
                error=f"Command blocked: {reason}",
                metadata={"security_mode": self.security_mode, "blocked": True}
            )

        # Resolve working directory
        if not working_dir and self.workspace_dir:
            working_dir = str(self.workspace_dir)
        
        # Build environment with PATH prepend
        env = self._build_env()

        try:
            # Create subprocess
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=working_dir,
                env=env,
            )

            # Wait for completion with configurable timeout
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(), 
                    timeout=self.timeout_sec
                )
            except TimeoutError:
                process.kill()
                return ToolResult(
                    success=False, 
                    content="", 
                    error=f"Command timed out after {self.timeout_sec} seconds"
                )

            # Decode output
            stdout_text = stdout.decode("utf-8", errors="replace")
            stderr_text = stderr.decode("utf-8", errors="replace")

            # Combine output
            output = ""
            if stdout_text:
                output += stdout_text
            if stderr_text:
                if output:
                    output += "\n"
                output += stderr_text

            return ToolResult(
                success=process.returncode == 0,
                content=output,
                error=None if process.returncode == 0 else f"Exit code: {process.returncode}",
                metadata={
                    "exitCode": process.returncode,
                    "security_mode": self.security_mode,
                    "ask_mode": self.ask_mode,
                    "timeout_sec": self.timeout_sec,
                },
            )

        except Exception as e:
            logger.error(f"Bash tool error: {e}", exc_info=True)
            return ToolResult(success=False, content="", error=str(e))
    
    async def _wait_for_approval(self, approval_id: str) -> bool:
        """Wait for approval decision"""
        while True:
            request = self.approval_manager.get_approval(approval_id)
            if not request:
                return False
            
            if request.status == "approved":
                return True
            elif request.status in ["rejected", "expired"]:
                return False
            
            # Check again in 1 second
            await asyncio.sleep(1.0)
