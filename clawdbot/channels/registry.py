"""Channel registry"""

from typing import Optional
from .base import ChannelPlugin


class ChannelRegistry:
    """Registry of channel plugins"""

    def __init__(self):
        self._channels: dict[str, ChannelPlugin] = {}

    def register(self, channel: ChannelPlugin) -> None:
        """Register a channel"""
        self._channels[channel.id] = channel

    def get(self, channel_id: str) -> Optional[ChannelPlugin]:
        """Get channel by ID"""
        return self._channels.get(channel_id)

    def list_channels(self) -> list[ChannelPlugin]:
        """List all channels"""
        return list(self._channels.values())

    def list_running(self) -> list[ChannelPlugin]:
        """List running channels"""
        return [ch for ch in self._channels.values() if ch.is_running()]

    def unregister(self, channel_id: str) -> None:
        """Unregister a channel"""
        if channel_id in self._channels:
            del self._channels[channel_id]


# Global channel registry
_global_registry = ChannelRegistry()


def get_channel_registry() -> ChannelRegistry:
    """Get global channel registry"""
    return _global_registry
