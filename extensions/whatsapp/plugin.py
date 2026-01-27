"""WhatsApp channel plugin"""

from clawdbot.channels.whatsapp import WhatsAppChannel
from clawdbot.channels.registry import get_channel_registry


def register(api):
    """Register WhatsApp channel"""
    channel = WhatsAppChannel()
    registry = get_channel_registry()
    registry.register(channel)
