"""Extension runtime: holds loaded extensions and dispatches events.

Matches pi-mono ExtensionRuntime role. Does not implement full ExtensionContext
(UI, session manager, etc.); that is provided by the runner when binding to agent.
"""
from __future__ import annotations

import asyncio
import logging
from typing import Any, Callable

from .types import ExtensionContext

logger = logging.getLogger(__name__)


class ExtensionRuntime:
    """
    Runtime for extensions: stores tools and handlers, dispatches events.
    Runner binds context (agent_id, session_id, etc.) and invokes emit().
    """

    def __init__(self):
        self._tools: list[dict[str, Any]] = []
        self._handlers: dict[str, list[Callable[..., Any]]] = {}
        self._commands: dict[str, dict[str, Any]] = {}
        self._context: ExtensionContext | None = None

    def set_context(self, context: ExtensionContext) -> None:
        """Set the context passed to event handlers."""
        self._context = context

    def register_tools(self, tools: list[dict[str, Any]]) -> None:
        """Register tools from loaded extensions."""
        self._tools.extend(tools)

    def register_handlers(self, handlers: dict[str, list[Callable[..., Any]]]) -> None:
        """Merge handlers from loaded extensions."""
        for event, hlist in handlers.items():
            self._handlers.setdefault(event, []).extend(hlist)

    def register_commands(self, commands: dict[str, dict[str, Any]]) -> None:
        """Register commands from loaded extensions."""
        self._commands.update(commands)

    def get_tools(self) -> list[dict[str, Any]]:
        """Return all registered tools (for agent to use)."""
        return self._tools.copy()

    def get_commands(self) -> dict[str, dict[str, Any]]:
        """Return all registered commands."""
        return self._commands.copy()

    async def emit(self, event: str, payload: dict[str, Any] | None = None) -> list[Any]:
        """
        Dispatch event to all registered handlers. Returns list of results.
        """
        if self._context is None:
            logger.debug("ExtensionRuntime.emit(%s) skipped: no context", event)
            return []
        payload = payload or {}
        results: list[Any] = []
        for handler in self._handlers.get(event, []):
            try:
                if asyncio.iscoroutinefunction(handler):
                    r = await handler({**payload, "type": event}, self._context)
                else:
                    r = handler({**payload, "type": event}, self._context)
                if r is not None:
                    results.append(r)
            except Exception as e:
                logger.exception("Extension handler failed for %s: %s", event, e)
        return results
