"""Chrome DevTools Protocol (CDP) helper utilities

This module provides utilities for working with Chrome DevTools Protocol,
including command execution, event handling, and response parsing.
"""
from __future__ import annotations

import asyncio
import json
import logging
from typing import Any

logger = logging.getLogger(__name__)


class CDPError(Exception):
    """CDP command execution error"""
    pass


class CDPHelper:
    """Helper class for Chrome DevTools Protocol operations"""
    
    def __init__(self, websocket_url: str):
        """
        Initialize CDP helper
        
        Args:
            websocket_url: WebSocket URL for CDP connection
        """
        self.websocket_url = websocket_url
        self.ws = None
        self.command_id = 0
        self.pending_commands: dict[int, asyncio.Future] = {}
        self.event_handlers: dict[str, list[callable]] = {}
        
    async def connect(self) -> None:
        """Connect to CDP WebSocket"""
        try:
            import websockets
            self.ws = await websockets.connect(self.websocket_url)
            # Start message handler
            asyncio.create_task(self._handle_messages())
            logger.info(f"Connected to CDP: {self.websocket_url}")
        except Exception as e:
            logger.error(f"Failed to connect to CDP: {e}")
            raise CDPError(f"Connection failed: {e}")
    
    async def disconnect(self) -> None:
        """Disconnect from CDP"""
        if self.ws:
            await self.ws.close()
            self.ws = None
            logger.info("Disconnected from CDP")
    
    async def execute_command(
        self,
        method: str,
        params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """
        Execute CDP command
        
        Args:
            method: CDP method name (e.g., "Page.navigate")
            params: Command parameters
            
        Returns:
            Command result
            
        Raises:
            CDPError: If command fails
        """
        if not self.ws:
            raise CDPError("Not connected to CDP")
        
        self.command_id += 1
        command = {
            "id": self.command_id,
            "method": method,
            "params": params or {}
        }
        
        # Create future for response
        future = asyncio.Future()
        self.pending_commands[self.command_id] = future
        
        try:
            # Send command
            await self.ws.send(json.dumps(command))
            
            # Wait for response (with timeout)
            result = await asyncio.wait_for(future, timeout=30.0)
            return result
            
        except asyncio.TimeoutError:
            del self.pending_commands[self.command_id]
            raise CDPError(f"Command timeout: {method}")
        except Exception as e:
            del self.pending_commands[self.command_id]
            raise CDPError(f"Command failed: {e}")
    
    async def _handle_messages(self) -> None:
        """Handle incoming CDP messages"""
        try:
            async for message in self.ws:
                data = json.loads(message)
                
                # Handle command responses
                if "id" in data:
                    cmd_id = data["id"]
                    if cmd_id in self.pending_commands:
                        future = self.pending_commands.pop(cmd_id)
                        
                        if "error" in data:
                            error = data["error"]
                            future.set_exception(
                                CDPError(f"{error.get('message', 'Unknown error')}")
                            )
                        else:
                            future.set_result(data.get("result", {}))
                
                # Handle events
                elif "method" in data:
                    method = data["method"]
                    params = data.get("params", {})
                    await self._dispatch_event(method, params)
                    
        except Exception as e:
            logger.error(f"Message handler error: {e}")
    
    def on_event(self, event_name: str, handler: callable) -> None:
        """
        Register event handler
        
        Args:
            event_name: CDP event name (e.g., "Page.loadEventFired")
            handler: Handler function
        """
        if event_name not in self.event_handlers:
            self.event_handlers[event_name] = []
        self.event_handlers[event_name].append(handler)
    
    def off_event(self, event_name: str, handler: callable) -> None:
        """
        Unregister event handler
        
        Args:
            event_name: CDP event name
            handler: Handler function to remove
        """
        if event_name in self.event_handlers:
            self.event_handlers[event_name].remove(handler)
    
    async def _dispatch_event(self, event_name: str, params: dict[str, Any]) -> None:
        """Dispatch event to handlers"""
        if event_name in self.event_handlers:
            for handler in self.event_handlers[event_name]:
                try:
                    await handler(params)
                except Exception as e:
                    logger.error(f"Event handler error: {e}")
    
    async def enable_domain(self, domain: str) -> None:
        """
        Enable CDP domain
        
        Args:
            domain: Domain name (e.g., "Page", "Network", "DOM")
        """
        await self.execute_command(f"{domain}.enable")
    
    async def disable_domain(self, domain: str) -> None:
        """
        Disable CDP domain
        
        Args:
            domain: Domain name
        """
        await self.execute_command(f"{domain}.disable")


async def get_browser_contexts(cdp: CDPHelper) -> list[dict[str, Any]]:
    """
    Get all browser contexts
    
    Args:
        cdp: CDP helper instance
        
    Returns:
        List of browser contexts
    """
    result = await cdp.execute_command("Target.getBrowserContexts")
    return result.get("browserContextIds", [])


async def create_target(
    cdp: CDPHelper,
    url: str,
    width: int = 1280,
    height: int = 720
) -> str:
    """
    Create new browser target (tab)
    
    Args:
        cdp: CDP helper instance
        url: URL to navigate to
        width: Viewport width
        height: Viewport height
        
    Returns:
        Target ID
    """
    result = await cdp.execute_command("Target.createTarget", {
        "url": url,
        "width": width,
        "height": height
    })
    return result["targetId"]


async def close_target(cdp: CDPHelper, target_id: str) -> None:
    """
    Close browser target
    
    Args:
        cdp: CDP helper instance
        target_id: Target ID to close
    """
    await cdp.execute_command("Target.closeTarget", {
        "targetId": target_id
    })


async def navigate_to_url(cdp: CDPHelper, url: str) -> None:
    """
    Navigate to URL
    
    Args:
        cdp: CDP helper instance
        url: URL to navigate to
    """
    await cdp.execute_command("Page.navigate", {"url": url})


async def get_document(cdp: CDPHelper) -> dict[str, Any]:
    """
    Get DOM document
    
    Args:
        cdp: CDP helper instance
        
    Returns:
        Document node
    """
    result = await cdp.execute_command("DOM.getDocument")
    return result["root"]


async def query_selector(
    cdp: CDPHelper,
    node_id: int,
    selector: str
) -> int | None:
    """
    Query selector on node
    
    Args:
        cdp: CDP helper instance
        node_id: Node ID to query from
        selector: CSS selector
        
    Returns:
        Node ID or None if not found
    """
    try:
        result = await cdp.execute_command("DOM.querySelector", {
            "nodeId": node_id,
            "selector": selector
        })
        return result.get("nodeId", 0) or None
    except CDPError:
        return None


async def evaluate_js(
    cdp: CDPHelper,
    expression: str,
    await_promise: bool = True
) -> Any:
    """
    Evaluate JavaScript expression
    
    Args:
        cdp: CDP helper instance
        expression: JavaScript expression
        await_promise: Whether to await promise results
        
    Returns:
        Evaluation result
    """
    result = await cdp.execute_command("Runtime.evaluate", {
        "expression": expression,
        "awaitPromise": await_promise,
        "returnByValue": True
    })
    
    if result.get("exceptionDetails"):
        raise CDPError(f"JS evaluation failed: {result['exceptionDetails']}")
    
    return result.get("result", {}).get("value")
