"""Discord channel plugin"""

from clawdbot.channels.discord import DiscordChannel
from clawdbot.channels.registry import get_channel_registry


def register(api):
    """Register Discord channel"""
    channel = DiscordChannel()
    registry = get_channel_registry()
    registry.register(channel)
