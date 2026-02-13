"""
Channel plugins for ClawdBot
"""

from .base import (
    ChannelCapabilities,
    ChannelPlugin,
    InboundMessage,
    MessageHandler,
    OutboundMessage,
)
from .connection import (
    ConnectionManager,
    ConnectionMetrics,
    ConnectionState,
    HealthChecker,
    ReconnectConfig,
)
from .registry import ChannelRegistry, get_channel, get_channel_registry, register_channel
from .webchat import WebChatChannel

# Import channel implementations conditionally
try:
    from .discord import DiscordChannel
except ImportError:
    DiscordChannel = None

try:
    from .slack import SlackChannel  
except ImportError:
    SlackChannel = None

try:
    from .telegram import TelegramChannel
except ImportError:
    TelegramChannel = None

__all__ = [
    # Base classes
    "ChannelPlugin",
    "ChannelCapabilities",
    "InboundMessage",
    "OutboundMessage",
    "MessageHandler",
    # Registry
    "ChannelRegistry",
    "get_channel_registry",
    "register_channel",
    "get_channel",
    # Connection management
    "ConnectionManager",
    "ConnectionState",
    "ConnectionMetrics",
    "ReconnectConfig",
    "HealthChecker",
    # Channels
    "WebChatChannel",
]

# Add optional channels to __all__ if they loaded
if TelegramChannel:
    __all__.append("TelegramChannel")
if DiscordChannel:
    __all__.append("DiscordChannel")
if SlackChannel:
    __all__.append("SlackChannel")
