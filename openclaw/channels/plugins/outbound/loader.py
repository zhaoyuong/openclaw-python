"""Outbound Adapter Loader

Load channel-specific outbound adapters.
Matches TypeScript implementation in src/channels/plugins/outbound/load.ts
"""

from __future__ import annotations

from typing import Any

from .telegram import TelegramOutboundAdapter
from .discord import DiscordOutboundAdapter
from .signal import SignalOutboundAdapter
from .slack import SlackOutboundAdapter


def load_outbound_adapter(channel: str) -> Any:
    """
    Load outbound adapter for channel.
    
    Args:
        channel: Channel name (telegram, discord, signal, slack, etc.)
        
    Returns:
        Outbound adapter instance
        
    Raises:
        ValueError: If channel not supported
        
    Example:
        >>> adapter = load_outbound_adapter("telegram")
        >>> result = await adapter.send_text("@user", "Hello")
    """
    adapters = {
        "telegram": TelegramOutboundAdapter,
        "discord": DiscordOutboundAdapter,
        "signal": SignalOutboundAdapter,
        "slack": SlackOutboundAdapter,
    }
    
    adapter_class = adapters.get(channel.lower())
    if not adapter_class:
        raise ValueError(f"Unsupported channel: {channel}")
    
    return adapter_class()
