"""Telegram channel plugin"""

from clawdbot.channels.telegram import TelegramChannel
from clawdbot.channels.registry import get_channel_registry


def register(api):
    """Register Telegram channel"""
    channel = TelegramChannel()
    registry = get_channel_registry()
    registry.register(channel)
