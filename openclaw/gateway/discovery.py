"""Gateway discovery service - mDNS/Bonjour advertising"""
from __future__ import annotations

import logging
import socket
from typing import Optional

logger = logging.getLogger(__name__)


class GatewayDiscovery:
    """Gateway discovery via mDNS/Bonjour"""
    
    def __init__(self, port: int = 18789, name: str = "OpenClaw Gateway"):
        self.port = port
        self.name = name
        self.zeroconf = None
        self.service_info = None
    
    async def start(self) -> None:
        """Start advertising gateway via mDNS"""
        try:
            from zeroconf import Zeroconf, ServiceInfo
            
            # Get local IP
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            
            # Create service info
            self.service_info = ServiceInfo(
                "_openclaw._tcp.local.",
                f"{self.name}._openclaw._tcp.local.",
                addresses=[socket.inet_aton(local_ip)],
                port=self.port,
                properties={
                    "version": "0.6.0",
                    "platform": "python"
                }
            )
            
            # Register service
            self.zeroconf = Zeroconf()
            self.zeroconf.register_service(self.service_info)
            
            logger.info(f"Gateway discovery started: {self.name} on port {self.port}")
        
        except ImportError:
            logger.warning("zeroconf not installed, discovery service disabled")
            logger.info("Install with: uv pip install zeroconf")
        except Exception as e:
            logger.error(f"Failed to start discovery service: {e}")
    
    async def stop(self) -> None:
        """Stop advertising"""
        if self.zeroconf and self.service_info:
            try:
                self.zeroconf.unregister_service(self.service_info)
                self.zeroconf.close()
                logger.info("Gateway discovery stopped")
            except Exception as e:
                logger.error(f"Failed to stop discovery: {e}")


async def start_gateway_discovery(port: int = 18789, name: str = "OpenClaw Gateway") -> Optional[GatewayDiscovery]:
    """Start gateway discovery service
    
    Args:
        port: Gateway port
        name: Service name
        
    Returns:
        GatewayDiscovery instance or None if failed
    """
    discovery = GatewayDiscovery(port, name)
    await discovery.start()
    return discovery


__all__ = ["GatewayDiscovery", "start_gateway_discovery"]
