"""Enhanced graceful shutdown for gateway server"""
from __future__ import annotations

import asyncio
import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


class GatewayShutdownHandler:
    """Manages graceful shutdown sequence"""
    
    def __init__(self, gateway_server):
        self.gateway = gateway_server
        self.shutdown_tasks: list[tuple[str, Any]] = []
    
    def register_cleanup(self, name: str, cleanup_func: Any) -> None:
        """Register a cleanup function"""
        self.shutdown_tasks.append((name, cleanup_func))
    
    async def shutdown(self) -> None:
        """Execute graceful shutdown sequence"""
        logger.info("Starting graceful shutdown...")
        
        # Shutdown sequence (matches TypeScript order)
        steps = [
            ("Broadcast shutdown event", self._broadcast_shutdown),
            ("Stop discovery service", self._stop_discovery),
            ("Stop Tailscale exposure", self._stop_tailscale),
            ("Stop channels", self._stop_channels),
            ("Stop plugin services", self._stop_plugins),
            ("Stop cron service", self._stop_cron),
            ("Stop heartbeat runner", self._stop_heartbeat),
            ("Clear maintenance timers", self._clear_timers),
            ("Close all connections", self._close_connections),
            ("Stop config reloader", self._stop_config_reloader),
            ("Close WebSocket server", self._close_ws_server),
            ("Close HTTP server", self._close_http_server),
        ]
        
        for step_name, step_func in steps:
            try:
                logger.info(f"Shutdown step: {step_name}")
                await step_func()
            except Exception as e:
                logger.error(f"Error in shutdown step '{step_name}': {e}")
        
        # Execute registered cleanups
        for name, cleanup_func in self.shutdown_tasks:
            try:
                logger.debug(f"Cleanup: {name}")
                if asyncio.iscoroutinefunction(cleanup_func):
                    await cleanup_func()
                else:
                    cleanup_func()
            except Exception as e:
                logger.error(f"Error in cleanup '{name}': {e}")
        
        logger.info("✅ Graceful shutdown complete")
    
    async def _broadcast_shutdown(self) -> None:
        """Broadcast shutdown event to all clients"""
        if hasattr(self.gateway, "broadcast_event"):
            try:
                await self.gateway.broadcast_event({
                    "type": "gateway.shutdown",
                    "message": "Gateway is shutting down"
                })
            except:
                pass
    
    async def _stop_discovery(self) -> None:
        """Stop discovery service"""
        if hasattr(self.gateway, "discovery") and self.gateway.discovery:
            await self.gateway.discovery.stop()
    
    async def _stop_tailscale(self) -> None:
        """Stop Tailscale exposure"""
        if hasattr(self.gateway, "tailscale") and self.gateway.tailscale:
            await self.gateway.tailscale.stop()
    
    async def _stop_channels(self) -> None:
        """Stop all channels"""
        if hasattr(self.gateway, "channel_manager"):
            await self.gateway.channel_manager.stop_all()
    
    async def _stop_plugins(self) -> None:
        """Stop plugin services"""
        # TODO: Implement plugin service stopping
        pass
    
    async def _stop_cron(self) -> None:
        """Stop cron service"""
        if hasattr(self.gateway, "cron") and self.gateway.cron:
            await self.gateway.cron.stop()
    
    async def _stop_heartbeat(self) -> None:
        """Stop heartbeat runner"""
        if hasattr(self.gateway, "heartbeat_runner") and self.gateway.heartbeat_runner:
            self.gateway.heartbeat_runner.stop()
    
    async def _clear_timers(self) -> None:
        """Clear maintenance timers"""
        # Clear any periodic tasks
        pass
    
    async def _close_connections(self) -> None:
        """Close all WebSocket connections"""
        if hasattr(self.gateway, "_connections"):
            for conn in list(self.gateway._connections):
                try:
                    await conn.close()
                except:
                    pass
    
    async def _stop_config_reloader(self) -> None:
        """Stop config file watcher"""
        if hasattr(self.gateway, "config_reloader") and self.gateway.config_reloader:
            await self.gateway.config_reloader.stop()
    
    async def _close_ws_server(self) -> None:
        """Close WebSocket server"""
        if hasattr(self.gateway, "ws_server") and self.gateway.ws_server:
            self.gateway.ws_server.close()
            await self.gateway.ws_server.wait_closed()
    
    async def _close_http_server(self) -> None:
        """Close HTTP server"""
        if hasattr(self.gateway, "http_server") and self.gateway.http_server:
            await self.gateway.http_server.shutdown()


def create_shutdown_handler(gateway_server) -> GatewayShutdownHandler:
    """Create shutdown handler for gateway
    
    Args:
        gateway_server: GatewayServer instance
        
    Returns:
        GatewayShutdownHandler
    """
    return GatewayShutdownHandler(gateway_server)


__all__ = ["GatewayShutdownHandler", "create_shutdown_handler"]
