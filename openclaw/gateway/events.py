"""
Gateway event broadcasting system

Provides event broadcasting to WebSocket clients with queuing support
for events that occur before the WebSocket server is ready.

Aligned with TypeScript broadcast pattern.
"""
from __future__ import annotations

import logging
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .server import GatewayServer

logger = logging.getLogger(__name__)


class GatewayBroadcaster:
    """
    Gateway event broadcasting system
    
    Features:
    - Broadcasts events to all connected WebSocket clients
    - Queues events before WebSocket server is ready
    - Supports dropIfSlow option to avoid blocking
    """
    
    def __init__(self):
        """Initialize broadcaster"""
        self._ws_server: 'GatewayServer | None' = None
        self._event_queue: list[tuple[str, Any, dict[str, Any] | None]] = []
        self._max_queue_size = 1000  # Prevent unbounded growth
        
        logger.debug("GatewayBroadcaster initialized")
    
    def set_ws_server(self, ws_server: 'GatewayServer') -> None:
        """
        Set WebSocket server for broadcasting
        
        Once set, flushes any queued events.
        
        Args:
            ws_server: WebSocket server instance
        """
        self._ws_server = ws_server
        logger.info(f"WebSocket server attached to broadcaster")
        
        # Flush queued events
        self._flush_queue()
    
    def broadcast(
        self, 
        event: str, 
        payload: Any, 
        opts: dict[str, Any] | None = None
    ) -> None:
        """
        Broadcast event to all connected clients
        
        If WebSocket server is not ready, queues the event for later.
        
        Args:
            event: Event name (e.g., "cron", "session.updated")
            payload: Event payload (any JSON-serializable data)
            opts: Options dict, may include:
                - dropIfSlow: bool - Skip slow clients to avoid blocking
        """
        opts = opts or {}
        
        if self._ws_server:
            # WebSocket server is ready, broadcast immediately
            try:
                self._ws_server.broadcast(event, payload, opts)
                logger.debug(f"Broadcast event: {event}")
            except Exception as e:
                logger.warning(f"Broadcast failed for event '{event}': {e}")
        else:
            # Queue event until WebSocket server is ready
            if len(self._event_queue) < self._max_queue_size:
                self._event_queue.append((event, payload, opts))
                logger.debug(f"Queued event (no WS server yet): {event}")
            else:
                logger.warning(f"Event queue full, dropping event: {event}")
    
    def _flush_queue(self) -> None:
        """Flush queued events to WebSocket server"""
        if not self._ws_server:
            logger.warning("Cannot flush queue: no WebSocket server")
            return
        
        if not self._event_queue:
            return
        
        logger.info(f"Flushing {len(self._event_queue)} queued events")
        
        flushed = 0
        failed = 0
        
        for event, payload, opts in self._event_queue:
            try:
                self._ws_server.broadcast(event, payload, opts)
                flushed += 1
            except Exception as e:
                logger.warning(f"Failed to flush event '{event}': {e}")
                failed += 1
        
        # Clear queue
        self._event_queue.clear()
        
        logger.info(f"Flushed {flushed} events ({failed} failed)")
    
    def get_queue_size(self) -> int:
        """Get current queue size"""
        return len(self._event_queue)
    
    def clear_queue(self) -> None:
        """Clear event queue without flushing"""
        count = len(self._event_queue)
        self._event_queue.clear()
        logger.info(f"Cleared {count} queued events")


# Global broadcaster instance
_broadcaster: GatewayBroadcaster | None = None


def get_broadcaster() -> GatewayBroadcaster:
    """
    Get global broadcaster instance
    
    Returns:
        Global GatewayBroadcaster instance
    """
    global _broadcaster
    
    if _broadcaster is None:
        _broadcaster = GatewayBroadcaster()
    
    return _broadcaster


def broadcast(event: str, payload: Any, opts: dict[str, Any] | None = None) -> None:
    """
    Broadcast event using global broadcaster
    
    Convenience function for broadcasting without getting broadcaster instance.
    
    Args:
        event: Event name
        payload: Event payload
        opts: Broadcast options
    """
    broadcaster = get_broadcaster()
    broadcaster.broadcast(event, payload, opts)


def set_ws_server(ws_server: 'GatewayServer') -> None:
    """
    Set WebSocket server for global broadcaster
    
    Args:
        ws_server: WebSocket server instance
    """
    broadcaster = get_broadcaster()
    broadcaster.set_ws_server(ws_server)
