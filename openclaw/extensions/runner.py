"""Extension runner: loads extensions and binds them to agent runtime.

Uses ExtensionLoader to discover/load, then ExtensionRuntime to hold state
and emit events. Agent integration: collect extension tools and wrap as AgentTool.
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from openclaw.agents.tools.base import AgentTool, ToolResult

from .loader import ExtensionLoader
from .runtime import ExtensionRuntime
from .types import ExtensionContext

logger = logging.getLogger(__name__)


class ExtensionToolAdapter(AgentTool):
    """
    Wraps an extension-registered tool so the agent can execute it.
    """

    def __init__(self, tool_def: dict[str, Any]):
        super().__init__()
        self.name = tool_def["name"]
        self.description = tool_def["description"]
        self._params_schema = tool_def.get("parameters", {"type": "object", "properties": {}})
        self._execute_fn = tool_def["execute"]
        self._extension_id = tool_def.get("extension_id", "unknown")

    def get_schema(self) -> dict[str, Any]:
        return self._params_schema

    async def _execute_impl(self, params: dict[str, Any]) -> ToolResult:
        import asyncio
        from openclaw.agents.abort import AbortSignal

        try:
            signal: AbortSignal | None = getattr(self, "_abort_signal", None)
            ctx: ExtensionContext | None = getattr(self, "_extension_context", None)
            fn = self._execute_fn
            if asyncio.iscoroutinefunction(fn):
                result = await fn(tool_call_id="", params=params, signal=signal, ctx=ctx)
            else:
                result = fn(tool_call_id="", params=params, signal=signal, ctx=ctx)
            if isinstance(result, ToolResult):
                return result
            if isinstance(result, dict):
                return ToolResult(
                    success=result.get("success", True),
                    content=result.get("content", str(result)),
                    error=result.get("error"),
                    metadata=result.get("metadata"),
                )
            return ToolResult(success=True, content=str(result))
        except Exception as e:
            logger.exception("Extension tool %s failed: %s", self.name, e)
            return ToolResult(success=False, content="", error=str(e))


class ExtensionRunner:
    """
    Discovers and loads extensions, builds runtime, and provides tools for the agent.
    """

    def __init__(
        self,
        workspace_root: Path | None = None,
        agent_id: str = "default",
        session_id: str | None = None,
        config: dict[str, Any] | None = None,
    ):
        self.workspace_root = workspace_root
        self.agent_id = agent_id
        self.session_id = session_id
        self.config = config or {}
        self._loader = ExtensionLoader(
            workspace_root=workspace_root,
            agent_id=agent_id,
            session_id=session_id,
            config=config,
        )
        self._runtime = ExtensionRuntime()

    def load(self) -> ExtensionRuntime:
        """
        Load all extensions and populate runtime. Returns the runtime so caller
        can set_context() and use get_tools() / emit().
        """
        apis = self._loader.load_all()
        all_tools: list[dict[str, Any]] = []
        all_handlers: dict[str, list] = {}
        all_commands: dict[str, dict[str, Any]] = {}
        for api in apis:
            all_tools.extend(api.get_tools())
            for evt, handlers in api.get_handlers().items():
                all_handlers.setdefault(evt, []).extend(handlers)
            all_commands.update(api.get_commands())
        self._runtime.register_tools(all_tools)
        self._runtime.register_handlers(all_handlers)
        self._runtime.register_commands(all_commands)
        return self._runtime

    def get_agent_tools(self, context: ExtensionContext | None = None) -> list[AgentTool]:
        """
        Return extension tools as AgentTool list for use in AgentLoop.
        """
        self._runtime.set_context(context or ExtensionContext(extension_dir=Path("."), agent_id=self.agent_id))
        agent_tools: list[AgentTool] = []
        for tool_def in self._runtime.get_tools():
            adapter = ExtensionToolAdapter(tool_def)
            if context is not None:
                adapter._extension_context = context  # noqa: SLF001
            agent_tools.append(adapter)
        return agent_tools

    def get_runtime(self) -> ExtensionRuntime:
        """Return the extension runtime (for emit, get_commands, etc.)."""
        return self._runtime

    def get_errors(self) -> list[tuple[str, str]]:
        """Return load errors from the loader."""
        return self._loader.get_errors()
