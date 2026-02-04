"""
Gateway WebSocket API

This module provides a standardized API for Gateway WebSocket methods.

Features:
- MethodRegistry for registering methods
- Automatic parameter validation
- Type-safe method definitions
- Auto-generated documentation

Usage:
    from openclaw.gateway.api import MethodRegistry, get_method_registry

    registry = get_method_registry()
    method = registry.get("connect")
    result = await method.execute(connection, params)
"""

from .methods import (
    AgentMethod,
    ChannelsListMethod,
    ConnectMethod,
    HealthMethod,
    PingMethod,
)
from .registry import GatewayMethod, MethodRegistry, get_method_registry

__all__ = [
    # Registry
    "MethodRegistry",
    "get_method_registry",
    "GatewayMethod",
    # Methods
    "ConnectMethod",
    "AgentMethod",
    "PingMethod",
    "HealthMethod",
    "ChannelsListMethod",
]
