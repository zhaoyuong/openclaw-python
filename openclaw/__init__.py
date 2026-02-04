"""
OpenClaw Python - Personal AI Assistant Platform

A Python implementation of the OpenClaw personal AI assistant platform.

Example usage:
    from openclaw import RuntimeEnv, Event, EventType
    from pathlib import Path

    # Create runtime environment
    env = RuntimeEnv(
        env_id="my-env",
        model="anthropic/claude-sonnet-4",
        workspace=Path("./workspace")
    )

    # Execute turn with unified events
    async for event in env.execute_turn("session-1", "Hello!"):
        if event.type == EventType.AGENT_TEXT:
            print(event.data.get("text", ""))
"""

__version__ = "0.6.0"
__author__ = "OpenClaw Contributors"

from .agents import AgentRuntime, Session, SessionManager
from .config import Settings, get_settings
from .config.unified import ConfigBuilder, OpenClawConfig

# Refactored modules (v0.6.0+)
from .events import Event, EventBus, EventType, get_event_bus
from .gateway.api import MethodRegistry, get_method_registry
from .monitoring import get_health_check, get_metrics, setup_logging
from .runtime_env import RuntimeEnv, RuntimeEnvManager, get_runtime_env_manager

__all__ = [
    # Version
    "__version__",
    # Core (legacy)
    "AgentRuntime",
    "Session",
    "SessionManager",
    "get_settings",
    "Settings",
    "get_health_check",
    "get_metrics",
    "setup_logging",
    # Events (v0.6.0+)
    "Event",
    "EventType",
    "EventBus",
    "get_event_bus",
    # RuntimeEnv (v0.6.0+)
    "RuntimeEnv",
    "RuntimeEnvManager",
    "get_runtime_env_manager",
    # Configuration (v0.6.0+)
    "OpenClawConfig",
    "ConfigBuilder",
    # Gateway API (v0.6.0+)
    "MethodRegistry",
    "get_method_registry",
]
