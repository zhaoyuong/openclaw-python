"""Accessibility tree snapshots for browser automation

This module provides utilities for capturing and analyzing accessibility tree
snapshots, which are useful for understanding page structure and interactive elements.
"""
from __future__ import annotations

import logging
from typing import Any

from .cdp_helpers import CDPHelper

logger = logging.getLogger(__name__)


class AccessibilityError(Exception):
    """Accessibility tree error"""
    pass


class AXNode:
    """Accessibility tree node"""
    
    def __init__(self, data: dict[str, Any]):
        """
        Initialize AX node from CDP data
        
        Args:
            data: Node data from CDP
        """
        self.node_id: str = data.get("nodeId", "")
        self.ignored: bool = data.get("ignored", False)
        self.role: str = data.get("role", {}).get("value", "")
        self.name: str = data.get("name", {}).get("value", "")
        self.description: str = data.get("description", {}).get("value", "")
        self.value: str = data.get("value", {}).get("value", "")
        self.properties: list[dict] = data.get("properties", [])
        self.child_ids: list[str] = data.get("childIds", [])
        self.backend_dom_node_id: int | None = data.get("backendDOMNodeId")
        
        # Parse properties
        self.prop_dict: dict[str, Any] = {}
        for prop in self.properties:
            prop_name = prop.get("name", "")
            prop_value = prop.get("value", {}).get("value")
            if prop_name:
                self.prop_dict[prop_name] = prop_value
    
    def is_interactive(self) -> bool:
        """Check if node is interactive"""
        interactive_roles = {
            "button", "link", "textbox", "searchbox", "combobox",
            "listbox", "menu", "menubar", "menuitem", "tab",
            "checkbox", "radio", "switch", "slider"
        }
        return self.role.lower() in interactive_roles
    
    def is_focusable(self) -> bool:
        """Check if node is focusable"""
        return self.prop_dict.get("focusable", False)
    
    def is_editable(self) -> bool:
        """Check if node is editable"""
        return self.prop_dict.get("editable") == "plaintext"
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary"""
        return {
            "nodeId": self.node_id,
            "role": self.role,
            "name": self.name,
            "description": self.description,
            "value": self.value,
            "ignored": self.ignored,
            "interactive": self.is_interactive(),
            "focusable": self.is_focusable(),
            "editable": self.is_editable(),
            "properties": self.prop_dict,
            "childIds": self.child_ids,
        }
    
    def __repr__(self) -> str:
        return f"AXNode(role={self.role}, name={self.name})"


class AccessibilityTree:
    """Accessibility tree snapshot"""
    
    def __init__(self, nodes: list[AXNode]):
        """
        Initialize accessibility tree
        
        Args:
            nodes: List of AX nodes
        """
        self.nodes = nodes
        self.nodes_by_id: dict[str, AXNode] = {
            node.node_id: node for node in nodes
        }
        self.root: AXNode | None = nodes[0] if nodes else None
    
    def find_by_role(self, role: str) -> list[AXNode]:
        """
        Find nodes by role
        
        Args:
            role: Role to search for
            
        Returns:
            List of matching nodes
        """
        return [node for node in self.nodes if node.role.lower() == role.lower()]
    
    def find_by_name(self, name: str, exact: bool = False) -> list[AXNode]:
        """
        Find nodes by name
        
        Args:
            name: Name to search for
            exact: Require exact match (default: partial match)
            
        Returns:
            List of matching nodes
        """
        if exact:
            return [node for node in self.nodes if node.name == name]
        else:
            name_lower = name.lower()
            return [node for node in self.nodes if name_lower in node.name.lower()]
    
    def find_interactive(self) -> list[AXNode]:
        """
        Find all interactive nodes
        
        Returns:
            List of interactive nodes
        """
        return [node for node in self.nodes if node.is_interactive()]
    
    def find_focusable(self) -> list[AXNode]:
        """
        Find all focusable nodes
        
        Returns:
            List of focusable nodes
        """
        return [node for node in self.nodes if node.is_focusable()]
    
    def get_children(self, node: AXNode) -> list[AXNode]:
        """
        Get children of node
        
        Args:
            node: Parent node
            
        Returns:
            List of child nodes
        """
        return [
            self.nodes_by_id[child_id]
            for child_id in node.child_ids
            if child_id in self.nodes_by_id
        ]
    
    def to_dict(self) -> dict[str, Any]:
        """Convert tree to dictionary"""
        return {
            "nodes": [node.to_dict() for node in self.nodes],
            "nodeCount": len(self.nodes),
        }
    
    def __len__(self) -> int:
        return len(self.nodes)
    
    def __repr__(self) -> str:
        return f"AccessibilityTree(nodes={len(self.nodes)})"


async def get_accessibility_tree(
    cdp: CDPHelper,
    fetch_relative: bool = False
) -> AccessibilityTree:
    """
    Get full accessibility tree snapshot
    
    Args:
        cdp: CDP helper instance
        fetch_relative: Fetch relative (vs absolute) tree
        
    Returns:
        Accessibility tree
        
    Raises:
        AccessibilityError: If snapshot fails
    """
    try:
        result = await cdp.execute_command("Accessibility.getFullAXTree", {
            "depth": -1,  # Full tree
            "frameId": None,  # Current frame
        })
        
        nodes = [AXNode(node_data) for node_data in result.get("nodes", [])]
        return AccessibilityTree(nodes)
        
    except Exception as e:
        logger.error(f"Failed to get accessibility tree: {e}")
        raise AccessibilityError(f"Snapshot failed: {e}")


async def get_partial_ax_tree(
    cdp: CDPHelper,
    node_id: int | None = None,
    backend_node_id: int | None = None,
    object_id: str | None = None,
    fetch_relatives: bool = False
) -> AccessibilityTree:
    """
    Get partial accessibility tree for specific node
    
    Args:
        cdp: CDP helper instance
        node_id: DOM node ID
        backend_node_id: Backend DOM node ID
        object_id: Remote object ID
        fetch_relatives: Include ancestor and sibling nodes
        
    Returns:
        Partial accessibility tree
        
    Raises:
        AccessibilityError: If snapshot fails
    """
    try:
        params: dict[str, Any] = {
            "fetchRelatives": fetch_relatives
        }
        
        if node_id is not None:
            params["nodeId"] = node_id
        elif backend_node_id is not None:
            params["backendNodeId"] = backend_node_id
        elif object_id is not None:
            params["objectId"] = object_id
        
        result = await cdp.execute_command("Accessibility.getPartialAXTree", params)
        
        nodes = [AXNode(node_data) for node_data in result.get("nodes", [])]
        return AccessibilityTree(nodes)
        
    except Exception as e:
        logger.error(f"Failed to get partial AX tree: {e}")
        raise AccessibilityError(f"Partial snapshot failed: {e}")


async def query_ax_tree(
    cdp: CDPHelper,
    node_id: int | None = None,
    backend_node_id: int | None = None,
    object_id: str | None = None,
    accessible_name: str | None = None,
    role: str | None = None,
) -> list[int]:
    """
    Query accessibility tree for nodes matching criteria
    
    Args:
        cdp: CDP helper instance
        node_id: DOM node ID to query from
        backend_node_id: Backend DOM node ID to query from
        object_id: Remote object ID to query from
        accessible_name: Accessible name to match
        role: Role to match
        
    Returns:
        List of matching backend node IDs
        
    Raises:
        AccessibilityError: If query fails
    """
    try:
        params: dict[str, Any] = {}
        
        if node_id is not None:
            params["nodeId"] = node_id
        elif backend_node_id is not None:
            params["backendNodeId"] = backend_node_id
        elif object_id is not None:
            params["objectId"] = object_id
        
        if accessible_name:
            params["accessibleName"] = accessible_name
        if role:
            params["role"] = role
        
        result = await cdp.execute_command("Accessibility.queryAXTree", params)
        
        return [node["backendDOMNodeId"] for node in result.get("nodes", [])]
        
    except Exception as e:
        logger.error(f"Failed to query AX tree: {e}")
        raise AccessibilityError(f"Query failed: {e}")


def format_ax_tree(tree: AccessibilityTree, max_depth: int = 5) -> str:
    """
    Format accessibility tree as readable text
    
    Args:
        tree: Accessibility tree
        max_depth: Maximum depth to display
        
    Returns:
        Formatted tree string
    """
    if not tree.root:
        return "Empty tree"
    
    lines: list[str] = []
    
    def format_node(node: AXNode, depth: int, prefix: str = "") -> None:
        if depth > max_depth:
            return
        
        # Format node info
        parts = [node.role]
        if node.name:
            parts.append(f'"{node.name}"')
        if node.value:
            parts.append(f"value={node.value}")
        
        markers = []
        if node.is_interactive():
            markers.append("interactive")
        if node.is_focusable():
            markers.append("focusable")
        if node.is_editable():
            markers.append("editable")
        
        if markers:
            parts.append(f"[{', '.join(markers)}]")
        
        lines.append(f"{prefix}{' '.join(parts)}")
        
        # Format children
        children = tree.get_children(node)
        for i, child in enumerate(children):
            is_last = i == len(children) - 1
            child_prefix = prefix + ("└─ " if is_last else "├─ ")
            next_prefix = prefix + ("   " if is_last else "│  ")
            format_node(child, depth + 1, child_prefix)
    
    format_node(tree.root, 0)
    return "\n".join(lines)
