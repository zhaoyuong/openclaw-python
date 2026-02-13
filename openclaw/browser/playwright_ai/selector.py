"""AI-powered element selection for browser automation

This module uses AI/LLM to intelligently select page elements based on
natural language descriptions, accessibility information, and visual features.
"""
from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


class AISelector:
    """AI-powered element selector"""
    
    def __init__(self, provider: Any = None):
        """
        Initialize AI selector
        
        Args:
            provider: LLM provider for element selection
        """
        self.provider = provider
    
    async def select_element(
        self,
        page_context: dict[str, Any],
        description: str,
        screenshot: bytes | None = None,
    ) -> dict[str, Any] | None:
        """
        Select element using AI based on description
        
        Args:
            page_context: Page context (DOM, accessibility tree, etc.)
            description: Natural language description of target element
            screenshot: Optional screenshot for visual analysis
            
        Returns:
            Element information or None if not found
        """
        # Extract candidates from page context
        candidates = self._extract_candidates(page_context)
        
        if not candidates:
            logger.warning("No interactive elements found")
            return None
        
        # Score candidates based on description
        scored = await self._score_candidates(candidates, description, screenshot)
        
        if not scored:
            return None
        
        # Return best match
        best_match = max(scored, key=lambda x: x["score"])
        
        if best_match["score"] > 0.5:  # Confidence threshold
            return best_match["element"]
        
        return None
    
    def _extract_candidates(self, page_context: dict[str, Any]) -> list[dict[str, Any]]:
        """
        Extract candidate elements from page context
        
        Args:
            page_context: Page context
            
        Returns:
            List of candidate elements
        """
        candidates = []
        
        # Extract from accessibility tree
        if "accessibility" in page_context:
            ax_tree = page_context["accessibility"]
            for node in ax_tree.get("nodes", []):
                if node.get("interactive") or node.get("focusable"):
                    candidates.append({
                        "type": "ax_node",
                        "role": node.get("role", ""),
                        "name": node.get("name", ""),
                        "description": node.get("description", ""),
                        "nodeId": node.get("nodeId"),
                        "backendDOMNodeId": node.get("backendDOMNodeId"),
                    })
        
        # Extract from DOM
        if "dom" in page_context:
            # Add DOM-based candidates
            pass
        
        return candidates
    
    async def _score_candidates(
        self,
        candidates: list[dict[str, Any]],
        description: str,
        screenshot: bytes | None = None,
    ) -> list[dict[str, float]]:
        """
        Score candidates based on description match
        
        Args:
            candidates: List of candidate elements
            description: Target description
            screenshot: Optional screenshot
            
        Returns:
            List of {element, score} dicts
        """
        if not self.provider:
            # Fallback: simple text matching
            return self._fallback_scoring(candidates, description)
        
        # Use LLM for intelligent scoring
        # TODO: Implement LLM-based scoring
        return self._fallback_scoring(candidates, description)
    
    def _fallback_scoring(
        self,
        candidates: list[dict[str, Any]],
        description: str
    ) -> list[dict[str, Any]]:
        """
        Fallback scoring using simple text matching
        
        Args:
            candidates: List of candidates
            description: Target description
            
        Returns:
            Scored candidates
        """
        desc_lower = description.lower()
        scored = []
        
        for candidate in candidates:
            score = 0.0
            
            # Check role match
            role = candidate.get("role", "").lower()
            if role in desc_lower:
                score += 0.3
            
            # Check name match
            name = candidate.get("name", "").lower()
            if name and desc_lower in name:
                score += 0.5
            elif name and any(word in name for word in desc_lower.split()):
                score += 0.3
            
            # Check description match
            elem_desc = candidate.get("description", "").lower()
            if elem_desc and desc_lower in elem_desc:
                score += 0.2
            
            scored.append({
                "element": candidate,
                "score": min(score, 1.0)
            })
        
        return scored


async def select_element_by_description(
    page_context: dict[str, Any],
    description: str,
    screenshot: bytes | None = None,
    provider: Any = None,
) -> dict[str, Any] | None:
    """
    Select element by natural language description
    
    Args:
        page_context: Page context with DOM/accessibility info
        description: Natural language description
        screenshot: Optional screenshot
        provider: Optional LLM provider
        
    Returns:
        Element information or None
    """
    selector = AISelector(provider=provider)
    return await selector.select_element(page_context, description, screenshot)


async def click_element_by_description(
    cdp: Any,
    page_context: dict[str, Any],
    description: str,
) -> bool:
    """
    Click element by description
    
    Args:
        cdp: CDP helper
        page_context: Page context
        description: Element description
        
    Returns:
        True if clicked successfully
    """
    element = await select_element_by_description(page_context, description)
    
    if not element:
        logger.warning(f"Element not found: {description}")
        return False
    
    # Get backend DOM node ID
    backend_node_id = element.get("backendDOMNodeId")
    if not backend_node_id:
        return False
    
    # Convert to node ID
    result = await cdp.execute_command("DOM.describeNode", {
        "backendNodeId": backend_node_id
    })
    node_id = result["node"]["nodeId"]
    
    # Get element center
    box_model = await cdp.execute_command("DOM.getBoxModel", {
        "nodeId": node_id
    })
    
    quad = box_model["model"]["border"]
    xs = [quad[i] for i in range(0, len(quad), 2)]
    ys = [quad[i] for i in range(1, len(quad), 2)]
    
    center_x = sum(xs) / len(xs)
    center_y = sum(ys) / len(ys)
    
    # Click
    await cdp.execute_command("Input.dispatchMouseEvent", {
        "type": "mousePressed",
        "x": center_x,
        "y": center_y,
        "button": "left",
        "clickCount": 1
    })
    
    await cdp.execute_command("Input.dispatchMouseEvent", {
        "type": "mouseReleased",
        "x": center_x,
        "y": center_y,
        "button": "left",
        "clickCount": 1
    })
    
    logger.info(f"Clicked element: {description}")
    return True


async def fill_input_by_description(
    cdp: Any,
    page_context: dict[str, Any],
    description: str,
    text: str,
) -> bool:
    """
    Fill input field by description
    
    Args:
        cdp: CDP helper
        page_context: Page context
        description: Input field description
        text: Text to fill
        
    Returns:
        True if filled successfully
    """
    # Click on input first
    if not await click_element_by_description(cdp, page_context, description):
        return False
    
    # Type text
    for char in text:
        await cdp.execute_command("Input.dispatchKeyEvent", {
            "type": "char",
            "text": char
        })
    
    logger.info(f"Filled input '{description}' with text")
    return True
