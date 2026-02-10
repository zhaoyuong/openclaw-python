"""Channel adapter interfaces

Unified interface for channel outbound adapters.
Matches TypeScript src/channels/plugins/types.adapters.ts
"""
from dataclasses import dataclass
from typing import Protocol, Optional, Callable, Dict, Any


@dataclass
class ChannelOutboundContext:
    """
    Context for outbound messages
    
    Matches TypeScript ChannelOutboundContext
    """
    cfg: dict
    to: str
    text: str
    media_url: Optional[str] = None
    gif_playback: bool = False
    reply_to_id: Optional[str] = None
    thread_id: Optional[str] = None
    account_id: Optional[str] = None
    deps: Optional[Dict[str, Any]] = None


class ChannelOutboundAdapter(Protocol):
    """
    Protocol for channel outbound adapters
    
    All channels must implement this interface.
    Matches TypeScript ChannelOutboundAdapter
    """
    
    # Delivery mode: "direct", "gateway", or "hybrid"
    delivery_mode: str
    
    # Optional chunker function
    chunker: Optional[Callable[[str, int], list[str]]] = None
    
    # Chunker mode: "text" or "markdown"
    chunker_mode: str = "text"
    
    # Text chunk limit (characters)
    text_chunk_limit: int = 4000
    
    # Max poll options
    poll_max_options: Optional[int] = None
    
    async def send_text(self, ctx: ChannelOutboundContext) -> Dict[str, Any]:
        """
        Send text message
        
        Returns:
            Delivery result dict
        """
        ...
    
    async def send_media(self, ctx: ChannelOutboundContext) -> Dict[str, Any]:
        """
        Send media message (image, video, etc.)
        
        Returns:
            Delivery result dict
        """
        ...
    
    async def send_payload(self, ctx: ChannelOutboundContext, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send complete payload (text + media)
        
        Optional method for channels that can handle
        combined payloads.
        
        Returns:
            Delivery result dict
        """
        ...


@dataclass
class OutboundDeliveryResult:
    """Result of outbound message delivery"""
    success: bool
    message_id: Optional[str] = None
    error: Optional[str] = None
    delivered_count: int = 0
    chunk_count: int = 0


# Channel adapter registry
_adapters: Dict[str, ChannelOutboundAdapter] = {}


def register_adapter(channel: str, adapter: ChannelOutboundAdapter):
    """Register a channel adapter"""
    _adapters[channel] = adapter


def get_adapter(channel: str) -> Optional[ChannelOutboundAdapter]:
    """Get adapter for channel"""
    return _adapters.get(channel)


def list_adapters() -> list[str]:
    """List registered adapters"""
    return list(_adapters.keys())
