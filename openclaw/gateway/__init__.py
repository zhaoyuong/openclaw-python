"""
Gateway WebSocket server implementation

The Gateway provides:
1. ChannelManager - Manages channel plugins (Telegram, Discord, etc.)
2. WebSocket API - Serves external clients (UI, CLI, mobile)
3. Event Broadcasting - Broadcasts Agent events to all clients

Architecture:
    Gateway Server
        ├── ChannelManager (manages channel plugins)
        ├── WebSocket Server (for external clients)
        └── Event Broadcasting (Observer Pattern)
"""

from .channel_manager import (
    ChannelEventListener,
    ChannelManager,
    ChannelRuntimeEnv,
    ChannelState,
    discover_channel_plugins,
    load_channel_plugins,
)
from .protocol import (
    ErrorShape,
    EventFrame,
    RequestFrame,
    ResponseFrame,
)
from .server import GatewayConnection, GatewayServer

__all__ = [
    # Server
    "GatewayServer",
    "GatewayConnection",
    # Channel Manager
    "ChannelManager",
    "ChannelState",
    "ChannelRuntimeEnv",
    "ChannelEventListener",
    "discover_channel_plugins",
    "load_channel_plugins",
    # Protocol
    "RequestFrame",
    "ResponseFrame",
    "EventFrame",
    "ErrorShape",
]
