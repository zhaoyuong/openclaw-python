"""Base channel plugin interface"""

from abc import ABC, abstractmethod
from typing import Any, Optional, Callable, Awaitable
from pydantic import BaseModel


class ChannelCapabilities(BaseModel):
    """Channel capabilities"""

    chat_types: list[str] = ["direct", "group"]  # Supported chat types
    supports_media: bool = False
    supports_reactions: bool = False
    supports_threads: bool = False
    supports_polls: bool = False


class InboundMessage(BaseModel):
    """Normalized inbound message"""

    channel_id: str
    message_id: str
    sender_id: str
    sender_name: str
    chat_id: str
    chat_type: str  # "direct", "group", "channel"
    text: str
    timestamp: str
    reply_to: Optional[str] = None
    metadata: dict[str, Any] = {}


class OutboundMessage(BaseModel):
    """Message to send"""

    channel_id: str
    target: str  # Chat/user ID
    text: str
    reply_to: Optional[str] = None
    metadata: dict[str, Any] = {}


# Type alias for message handler
MessageHandler = Callable[[InboundMessage], Awaitable[None]]


class ChannelPlugin(ABC):
    """Base class for channel plugins"""

    def __init__(self):
        self.id: str = ""
        self.label: str = ""
        self.capabilities: ChannelCapabilities = ChannelCapabilities()
        self._message_handler: Optional[MessageHandler] = None
        self._running: bool = False

    @abstractmethod
    async def start(self, config: dict[str, Any]) -> None:
        """Start the channel"""
        pass

    @abstractmethod
    async def stop(self) -> None:
        """Stop the channel"""
        pass

    @abstractmethod
    async def send_text(self, target: str, text: str, reply_to: Optional[str] = None) -> str:
        """Send text message. Returns message ID."""
        pass

    async def send_media(
        self,
        target: str,
        media_url: str,
        media_type: str,
        caption: Optional[str] = None
    ) -> str:
        """Send media message. Returns message ID."""
        raise NotImplementedError("Media not supported by this channel")

    def set_message_handler(self, handler: MessageHandler) -> None:
        """Set handler for inbound messages"""
        self._message_handler = handler

    async def _handle_message(self, message: InboundMessage) -> None:
        """Internal message handler"""
        if self._message_handler:
            await self._message_handler(message)

    def is_running(self) -> bool:
        """Check if channel is running"""
        return self._running

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "label": self.label,
            "capabilities": self.capabilities.model_dump(),
            "running": self._running
        }
