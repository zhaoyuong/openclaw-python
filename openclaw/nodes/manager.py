"""
Node management service

Manages distributed node registration, pairing, and command invocation.
"""

import logging
import secrets
import time
from typing import Any, Dict, Optional, List
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class NodeInfo:
    """Node information"""
    id: str
    capabilities: Dict[str, Any] = field(default_factory=dict)
    registered_at: float = field(default_factory=time.time)
    status: str = "active"  # active | inactive | error
    public_key: Optional[str] = None
    last_seen: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PairRequest:
    """Node pairing request"""
    node_id: str
    nonce: str
    signature: str
    requested_at: float = field(default_factory=time.time)
    status: str = "pending"  # pending | approved | rejected
    token: Optional[str] = None


class NodeManager:
    """
    Node management service
    
    Handles:
    - Node registration
    - Node pairing/authentication
    - Command invocation
    - Node status tracking
    """
    
    def __init__(self):
        """Initialize node manager"""
        self.nodes: Dict[str, NodeInfo] = {}
        self.pending_pairs: Dict[str, PairRequest] = {}
        self.tokens: Dict[str, str] = {}  # token -> node_id mapping
    
    def register_node(
        self,
        node_id: str,
        capabilities: Dict[str, Any],
        public_key: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> NodeInfo:
        """
        Register a node
        
        Args:
            node_id: Node identifier
            capabilities: Node capabilities
            public_key: Node public key for authentication
            metadata: Additional metadata
            
        Returns:
            NodeInfo
        """
        node = NodeInfo(
            id=node_id,
            capabilities=capabilities,
            public_key=public_key,
            metadata=metadata or {}
        )
        
        self.nodes[node_id] = node
        logger.info(f"Registered node: {node_id}")
        
        return node
    
    def request_pairing(
        self,
        node_id: str,
        nonce: str,
        signature: str
    ) -> PairRequest:
        """
        Request node pairing
        
        Args:
            node_id: Node identifier
            nonce: Nonce for replay protection
            signature: Signature of nonce
            
        Returns:
            PairRequest
        """
        request = PairRequest(
            node_id=node_id,
            nonce=nonce,
            signature=signature
        )
        
        self.pending_pairs[node_id] = request
        logger.info(f"Node pairing requested: {node_id}")
        
        # TODO: Broadcast node.pair.requested event
        
        return request
    
    def approve_pairing(self, node_id: str) -> Optional[str]:
        """
        Approve node pairing
        
        Args:
            node_id: Node identifier
            
        Returns:
            Access token or None if request not found
        """
        request = self.pending_pairs.get(node_id)
        if not request:
            logger.warning(f"No pending pair request for node: {node_id}")
            return None
        
        # Generate token
        token = secrets.token_urlsafe(32)
        request.status = "approved"
        request.token = token
        
        # Store token mapping
        self.tokens[token] = node_id
        
        # Remove from pending
        del self.pending_pairs[node_id]
        
        logger.info(f"Node pairing approved: {node_id}")
        
        # TODO: Broadcast node.pair.resolved event
        
        return token
    
    def reject_pairing(self, node_id: str, reason: Optional[str] = None):
        """
        Reject node pairing
        
        Args:
            node_id: Node identifier
            reason: Rejection reason
        """
        request = self.pending_pairs.get(node_id)
        if not request:
            logger.warning(f"No pending pair request for node: {node_id}")
            return
        
        request.status = "rejected"
        
        # Remove from pending
        del self.pending_pairs[node_id]
        
        logger.info(f"Node pairing rejected: {node_id}, reason: {reason}")
        
        # TODO: Broadcast node.pair.rejected event
    
    def list_nodes(self) -> List[Dict[str, Any]]:
        """
        List all nodes
        
        Returns:
            List of node info dictionaries
        """
        nodes = []
        for node in self.nodes.values():
            nodes.append({
                "id": node.id,
                "capabilities": node.capabilities,
                "status": node.status,
                "registeredAt": node.registered_at,
                "lastSeen": node.last_seen,
                "metadata": node.metadata
            })
        return nodes
    
    def list_pending_pairs(self) -> List[Dict[str, Any]]:
        """
        List pending pairing requests
        
        Returns:
            List of pending pair requests
        """
        pairs = []
        for request in self.pending_pairs.values():
            pairs.append({
                "nodeId": request.node_id,
                "requestedAt": request.requested_at,
                "status": request.status
            })
        return pairs
    
    def get_node(self, node_id: str) -> Optional[NodeInfo]:
        """
        Get node by ID
        
        Args:
            node_id: Node identifier
            
        Returns:
            NodeInfo or None
        """
        return self.nodes.get(node_id)
    
    def verify_token(self, token: str) -> Optional[str]:
        """
        Verify node token
        
        Args:
            token: Access token
            
        Returns:
            Node ID or None if invalid
        """
        return self.tokens.get(token)
    
    async def invoke_node(
        self,
        node_id: str,
        command: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Invoke command on a node
        
        Args:
            node_id: Node identifier
            command: Command to execute
            params: Command parameters
            
        Returns:
            Command result
        """
        node = self.nodes.get(node_id)
        if not node:
            raise ValueError(f"Node not found: {node_id}")
        
        if node.status != "active":
            raise ValueError(f"Node is not active: {node_id}")
        
        # TODO: Send command to node via Gateway connection
        # For now, return a stub response
        logger.info(f"Invoking command on node {node_id}: {command}")
        
        return {
            "nodeId": node_id,
            "command": command,
            "status": "queued",
            "invocationId": secrets.token_urlsafe(16)
        }


# Global node manager instance
_node_manager: Optional[NodeManager] = None


def get_node_manager() -> NodeManager:
    """Get global node manager instance"""
    global _node_manager
    if _node_manager is None:
        _node_manager = NodeManager()
    return _node_manager


def set_node_manager(manager: NodeManager):
    """Set global node manager instance"""
    global _node_manager
    _node_manager = manager
