"""Gateway method handlers"""

from typing import Any, Callable, Optional, Awaitable
import logging

logger = logging.getLogger(__name__)

# Type alias for handler functions
Handler = Callable[[Any, dict[str, Any]], Awaitable[Any]]

# Registry of method handlers
_handlers: dict[str, Handler] = {}


def register_handler(method: str) -> Callable[[Handler], Handler]:
    """Decorator to register a method handler"""

    def decorator(func: Handler) -> Handler:
        _handlers[method] = func
        return func

    return decorator


def get_method_handler(method: str) -> Optional[Handler]:
    """Get handler for a method"""
    return _handlers.get(method)


# Core method handlers


@register_handler("health")
async def handle_health(connection: Any, params: dict[str, Any]) -> dict[str, Any]:
    """Health check"""
    return {
        "status": "ok",
        "uptime": 0,  # TODO: Track actual uptime
        "connections": len(connection.config.gateway.__dict__)
    }


@register_handler("status")
async def handle_status(connection: Any, params: dict[str, Any]) -> dict[str, Any]:
    """Get server status"""
    return {
        "gateway": {
            "running": True,
            "port": connection.config.gateway.port,
            "connections": 1  # TODO: Track actual connections
        },
        "agents": {
            "count": len(connection.config.agents.list) if connection.config.agents.list else 0
        },
        "channels": {
            "active": []  # TODO: Track active channels
        }
    }


@register_handler("config.get")
async def handle_config_get(connection: Any, params: dict[str, Any]) -> dict[str, Any]:
    """Get configuration"""
    return connection.config.model_dump(exclude_none=True)


@register_handler("sessions.list")
async def handle_sessions_list(connection: Any, params: dict[str, Any]) -> list[dict[str, Any]]:
    """List active sessions"""
    # TODO: Implement session management
    return []


@register_handler("channels.list")
async def handle_channels_list(connection: Any, params: dict[str, Any]) -> list[dict[str, Any]]:
    """List available channels"""
    # TODO: Implement channel registry
    return []


# Placeholder handlers for methods to be implemented


@register_handler("agent")
async def handle_agent(connection: Any, params: dict[str, Any]) -> dict[str, Any]:
    """Run agent turn"""
    # TODO: Implement agent execution
    return {
        "runId": "placeholder",
        "acceptedAt": "2026-01-27T00:00:00Z"
    }


@register_handler("chat.send")
async def handle_chat_send(connection: Any, params: dict[str, Any]) -> dict[str, Any]:
    """Send chat message"""
    # TODO: Implement chat sending
    return {"messageId": "placeholder"}


@register_handler("chat.history")
async def handle_chat_history(connection: Any, params: dict[str, Any]) -> list[dict[str, Any]]:
    """Get chat history"""
    # TODO: Implement chat history
    return []
