"""Channel Action Plugins

Channel-specific actions like send, react, delete, edit, etc.
"""

from __future__ import annotations

from .telegram import TelegramActions
from .discord import DiscordActions
from .signal import SignalActions

__all__ = [
    "TelegramActions",
    "DiscordActions",
    "SignalActions",
]
