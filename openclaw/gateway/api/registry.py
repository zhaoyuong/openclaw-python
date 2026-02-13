"""
Gateway Method Registry

Provides a centralized registry for all Gateway WebSocket API methods.
"""
from __future__ import annotations


import logging
from typing import Any, Protocol

logger = logging.getLogger(__name__)


class GatewayMethod(Protocol):
    """
    Protocol for Gateway API methods

    All Gateway methods must implement this interface.
    """

    name: str
    description: str
    category: str  # e.g., "connection", "agent", "channels", "system"

    async def execute(
        self,
        connection: Any,  # GatewayConnection
        params: dict[str, Any],
    ) -> Any:
        """
        Execute the method

        Args:
            connection: Gateway WebSocket connection
            params: Method parameters

        Returns:
            Method result

        Raises:
            Exception: On method execution error
        """
        ...

    def get_schema(self) -> dict[str, Any]:
        """
        Get JSON schema for method parameters

        Returns:
            JSON schema dict
        """
        ...


class MethodRegistry:
    """
    Registry for Gateway WebSocket API methods

    Features:
    - Register/unregister methods
    - Method lookup by name
    - List methods by category
    - Auto-generate API documentation

    Example:
        registry = MethodRegistry()
        registry.register(ConnectMethod())
        registry.register(AgentMethod())

        method = registry.get("agent")
        result = await method.execute(connection, params)
    """

    def __init__(self):
        self._methods: dict[str, GatewayMethod] = {}
        self._categories: dict[str, list[str]] = {}

        logger.info("MethodRegistry initialized")

    def register(self, method: GatewayMethod):
        """
        Register a Gateway method

        Args:
            method: Method instance to register

        Example:
            registry.register(ConnectMethod())
        """
        if method.name in self._methods:
            logger.warning(f"Method '{method.name}' already registered, overwriting")

        self._methods[method.name] = method

        # Track by category
        category = getattr(method, "category", "other")
        if category not in self._categories:
            self._categories[category] = []
        if method.name not in self._categories[category]:
            self._categories[category].append(method.name)

        logger.debug(f"Registered method: {method.name} (category: {category})")

    def unregister(self, method_name: str) -> bool:
        """
        Unregister a method

        Args:
            method_name: Name of method to unregister

        Returns:
            True if method was unregistered, False if not found
        """
        if method_name not in self._methods:
            return False

        method = self._methods[method_name]
        category = getattr(method, "category", "other")

        del self._methods[method_name]

        if category in self._categories:
            if method_name in self._categories[category]:
                self._categories[category].remove(method_name)

        logger.debug(f"Unregistered method: {method_name}")
        return True

    def get(self, method_name: str) -> GatewayMethod | None:
        """
        Get method by name

        Args:
            method_name: Method name

        Returns:
            Method instance or None if not found
        """
        return self._methods.get(method_name)

    def has(self, method_name: str) -> bool:
        """Check if method exists"""
        return method_name in self._methods

    def list_all(self) -> list[str]:
        """List all registered method names"""
        return sorted(self._methods.keys())

    def list_by_category(self, category: str) -> list[str]:
        """
        List methods in a category

        Args:
            category: Category name

        Returns:
            List of method names in category
        """
        return sorted(self._categories.get(category, []))

    def get_categories(self) -> list[str]:
        """Get all categories"""
        return sorted(self._categories.keys())

    def get_method_count(self) -> int:
        """Get total number of registered methods"""
        return len(self._methods)

    def generate_docs(self) -> dict[str, Any]:
        """
        Generate API documentation

        Returns:
            Dict with API documentation

        Example:
            docs = registry.generate_docs()
            print(docs["methods"]["connect"]["description"])
        """
        docs = {
            "total_methods": self.get_method_count(),
            "categories": {},
            "methods": {},
        }

        # Group by category
        for category in self.get_categories():
            methods = self.list_by_category(category)
            docs["categories"][category] = {
                "count": len(methods),
                "methods": methods,
            }

        # Method details
        for name, method in self._methods.items():
            docs["methods"][name] = {
                "name": method.name,
                "description": method.description,
                "category": getattr(method, "category", "other"),
                "schema": method.get_schema() if hasattr(method, "get_schema") else {},
            }

        return docs

    def to_dict(self) -> dict[str, Any]:
        """Convert registry to dictionary"""
        return {
            "total_methods": self.get_method_count(),
            "categories": {cat: len(methods) for cat, methods in self._categories.items()},
            "methods": list(self._methods.keys()),
        }

    def __repr__(self) -> str:
        return (
            f"MethodRegistry(methods={self.get_method_count()}, categories={len(self._categories)})"
        )


# =============================================================================
# Global Registry
# =============================================================================

_global_registry: MethodRegistry | None = None


def get_method_registry() -> MethodRegistry:
    """
    Get the global method registry

    Returns:
        Global MethodRegistry instance

    Example:
        registry = get_method_registry()
        method = registry.get("connect")
    """
    global _global_registry
    if _global_registry is None:
        _global_registry = MethodRegistry()
        # Auto-register core methods
        _register_core_methods(_global_registry)
    return _global_registry


def _register_core_methods(registry: MethodRegistry):
    """Register core Gateway methods"""
    from .methods import (
        AgentMethod,
        ChannelsListMethod,
        ConnectMethod,
        HealthMethod,
        PingMethod,
    )
    from .sessions_methods import (
        SessionsListMethod,
        SessionsPreviewMethod,
        SessionsResolveMethod,
        SessionsPatchMethod,
        SessionsResetMethod,
        SessionsDeleteMethod,
        SessionsCompactMethod,
    )

    # Core methods
    registry.register(ConnectMethod())
    registry.register(PingMethod())
    registry.register(HealthMethod())
    registry.register(AgentMethod())
    registry.register(ChannelsListMethod())
    
    # Session methods
    registry.register(SessionsListMethod())
    registry.register(SessionsPreviewMethod())
    registry.register(SessionsResolveMethod())
    registry.register(SessionsPatchMethod())
    registry.register(SessionsResetMethod())
    registry.register(SessionsDeleteMethod())
    registry.register(SessionsCompactMethod())

    logger.info(f"Registered {registry.get_method_count()} core methods")
