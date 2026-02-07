"""
Runtime parameter resolution for system prompt

Collects runtime information and resolves configuration parameters
for use in system prompt construction.
"""

from __future__ import annotations

import logging
import platform
import socket
import sys
from pathlib import Path

logger = logging.getLogger(__name__)


def build_system_prompt_params(
    config: dict | None = None, workspace_dir: Path | None = None, runtime: dict | None = None
) -> dict:
    """
    Build system prompt parameters

    Resolves timezone, repo root, and runtime information for use in
    the system prompt builder.

    Args:
        config: OpenClaw configuration dict
        workspace_dir: Workspace directory
        runtime: Runtime information dict (optional override)

    Returns:
        Dict with keys:
        - user_timezone: str | None
        - runtime_info: dict (agent_id, host, os, arch, python_version, model, channel)
        - repo_root: str | None
    """
    # Resolve user timezone from config
    user_timezone = None
    if config and hasattr(config, "agents"):
        if hasattr(config.agents, "defaults"):
            user_timezone = getattr(config.agents.defaults, "userTimezone", None)
    elif isinstance(config, dict):
        user_timezone = config.get("agents", {}).get("defaults", {}).get("userTimezone")

    # Get runtime info
    if not runtime:
        runtime = {}

    runtime_info = get_runtime_info(
        agent_id=runtime.get("agent_id"), model=runtime.get("model"), channel=runtime.get("channel")
    )

    # Find repo root
    repo_root = None
    if workspace_dir:
        repo_root = resolve_repo_root(workspace_dir)

    if repo_root:
        runtime_info["repo_root"] = str(repo_root)

    return {
        "user_timezone": user_timezone,
        "runtime_info": runtime_info,
        "repo_root": str(repo_root) if repo_root else None,
    }


def get_runtime_info(
    agent_id: str | None = None, model: str | None = None, channel: str | None = None
) -> dict:
    """
    Collect runtime information

    Args:
        agent_id: Agent identifier (optional)
        model: Model name (optional)
        channel: Channel name (optional)

    Returns:
        Dict with runtime information:
        - agent_id: str | None
        - host: str
        - os: str
        - arch: str
        - python_version: str
        - model: str | None
        - channel: str | None
    """
    # Get hostname
    try:
        host = socket.gethostname()
    except Exception:
        host = "unknown"

    # Get OS and architecture
    os_name = platform.system().lower()
    arch = platform.machine().lower()

    # Get Python version
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    return {
        "agent_id": agent_id,
        "host": host,
        "os": os_name,
        "arch": arch,
        "python_version": python_version,
        "model": model,
        "channel": channel,
    }


def resolve_repo_root(start_dir: Path) -> Path | None:
    """
    Find git repository root by walking up directories

    Args:
        start_dir: Directory to start searching from

    Returns:
        Path to git root, or None if not found
    """
    current = start_dir.resolve()

    # Walk up to 12 levels
    for _ in range(12):
        git_path = current / ".git"

        try:
            if git_path.exists() and (git_path.is_dir() or git_path.is_file()):
                logger.debug(f"Found git root: {current}")
                return current
        except Exception as e:
            logger.debug(f"Error checking .git at {current}: {e}")

        # Move to parent
        parent = current.parent
        if parent == current:
            # Reached filesystem root
            break
        current = parent

    logger.debug(f"No git root found starting from {start_dir}")
    return None


def resolve_user_timezone(timezone_config: str | None) -> str | None:
    """
    Resolve user timezone from config

    Args:
        timezone_config: Timezone string from config (e.g., "America/New_York")

    Returns:
        Resolved timezone string, or None
    """
    if not timezone_config:
        return None

    timezone = timezone_config.strip()

    if not timezone or timezone.lower() == "auto":
        # Try to detect system timezone
        try:
            import time

            if hasattr(time, "tzname"):
                return time.tzname[0]
        except Exception:
            pass
        return None

    return timezone
