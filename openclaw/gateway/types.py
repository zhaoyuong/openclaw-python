"""
Gateway types and dependency injection containers

Aligned with TypeScript gateway architecture
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from ..agents.providers import LLMProvider
    from ..agents.session import SessionManager
    from ..agents.tools.base import AgentTool
    from ..cron import CronService
    from .channel_manager import ChannelManager


@dataclass
class GatewayDeps:
    """
    Gateway dependency container
    
    Provides indirect access to dependencies to avoid circular dependencies
    and support lazy initialization.
    
    Aligned with TypeScript CliDeps pattern.
    """
    
    provider: LLMProvider
    """LLM provider for agent execution"""
    
    tools: list[AgentTool]
    """Available tools for agents"""
    
    session_manager: SessionManager
    """Session management"""
    
    get_channel_manager: Callable[[], 'ChannelManager | None']
    """Lazy access to channel manager (may not be ready at cron init time)"""
    
    # Additional optional dependencies
    config: dict[str, Any] | None = None
    """Runtime configuration"""
    
    workspace_dir: Path | None = None
    """Workspace directory"""
    
    def get_channels(self) -> dict[str, Any]:
        """
        Get channel registry
        
        Returns:
            Dictionary of channel_id -> channel instance
        """
        channel_manager = self.get_channel_manager()
        if channel_manager:
            return channel_manager.channels if hasattr(channel_manager, 'channels') else {}
        return {}


@dataclass
class GatewayCronState:
    """
    Cron service state returned by gateway builder
    
    Aligned with TypeScript GatewayCronState
    """
    
    cron: CronService
    """Cron service instance"""
    
    store_path: Path
    """Path to cron jobs store"""
    
    enabled: bool
    """Whether cron is enabled"""


# Type aliases for clarity
BroadcastFn = Callable[[str, Any, dict[str, Any] | None], None]
"""Broadcast function type: (event, payload, options) -> None"""

GetChannelManagerFn = Callable[[], 'ChannelManager | None']
"""Function to get channel manager (may return None if not ready)"""
