"""Tailscale support for gateway exposure"""
from __future__ import annotations

import asyncio
import logging
import subprocess
from typing import Literal, Optional

logger = logging.getLogger(__name__)


class TailscaleExposure:
    """Tailscale serve/funnel management"""
    
    def __init__(self, port: int = 18789, mode: Literal["serve", "funnel"] = "serve"):
        self.port = port
        self.mode = mode
        self.process: Optional[subprocess.Popen] = None
    
    async def start(self) -> bool:
        """Start Tailscale exposure"""
        try:
            # Check if tailscale is installed
            result = subprocess.run(
                ["tailscale", "version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                logger.warning("Tailscale not installed")
                return False
            
            # Start serve or funnel
            if self.mode == "serve":
                cmd = ["tailscale", "serve", str(self.port)]
            else:
                cmd = ["tailscale", "funnel", str(self.port)]
            
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            logger.info(f"Tailscale {self.mode} started on port {self.port}")
            return True
        
        except FileNotFoundError:
            logger.warning("Tailscale binary not found")
            return False
        except Exception as e:
            logger.error(f"Failed to start Tailscale {self.mode}: {e}")
            return False
    
    async def stop(self) -> None:
        """Stop Tailscale exposure"""
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
                logger.info(f"Tailscale {self.mode} stopped")
            except Exception as e:
                logger.error(f"Failed to stop Tailscale: {e}")
                if self.process:
                    self.process.kill()


async def start_tailscale_exposure(
    port: int = 18789,
    mode: Literal["serve", "funnel"] = "serve"
) -> Optional[TailscaleExposure]:
    """Start Tailscale exposure
    
    Args:
        port: Gateway port to expose
        mode: "serve" (Tailnet only) or "funnel" (public internet)
        
    Returns:
        TailscaleExposure instance or None if failed
    """
    exposure = TailscaleExposure(port, mode)
    success = await exposure.start()
    return exposure if success else None


__all__ = ["TailscaleExposure", "start_tailscale_exposure"]
