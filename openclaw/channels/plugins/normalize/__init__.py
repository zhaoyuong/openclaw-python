"""Message Normalization Plugins

Normalize channel-specific message formats and target IDs to standard format.
"""

from __future__ import annotations

from .telegram import normalize_telegram_target, looks_like_telegram_target
from .discord import normalize_discord_target, looks_like_discord_target
from .signal import normalize_signal_target, looks_like_signal_target
from .slack import normalize_slack_target, looks_like_slack_target

__all__ = [
    "normalize_telegram_target",
    "looks_like_telegram_target",
    "normalize_discord_target",
    "looks_like_discord_target",
    "normalize_signal_target",
    "looks_like_signal_target",
    "normalize_slack_target",
    "looks_like_slack_target",
]
