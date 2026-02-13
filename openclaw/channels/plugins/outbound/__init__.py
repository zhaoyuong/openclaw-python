"""Outbound Message Adapters

Channel-specific outbound message adapters for sending messages.
"""

from __future__ import annotations

from .telegram import TelegramOutboundAdapter
from .discord import DiscordOutboundAdapter
from .signal import SignalOutboundAdapter
from .slack import SlackOutboundAdapter
from .loader import load_outbound_adapter

__all__ = [
    "TelegramOutboundAdapter",
    "DiscordOutboundAdapter",
    "SignalOutboundAdapter",
    "SlackOutboundAdapter",
    "load_outbound_adapter",
]
