"""
Exec approval management

Manages command execution approval workflow.
"""

import logging
import secrets
import time
from typing import Any, Dict, Optional, List, Callable, Awaitable
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class ApprovalRequest:
    """Command approval request"""
    id: str
    command: str
    context: Dict[str, Any] = field(default_factory=dict)
    requested_at: float = field(default_factory=time.time)
    status: str = "pending"  # pending | approved | rejected | expired
    approved_by: Optional[str] = None
    resolved_at: Optional[float] = None


@dataclass
class ApprovalPolicy:
    """Approval policy for commands"""
    pattern: str  # Command pattern (regex or glob)
    auto_approve: bool = False
    require_approval: bool = True
    allowed_users: Optional[List[str]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


ApprovalCallback = Callable[[ApprovalRequest, bool], Awaitable[None]]


class ExecApprovalManager:
    """
    Exec approval management service
    
    Handles:
    - Approval request creation
    - Approval/rejection workflow
    - Policy management
    - Event broadcasting
    """
    
    def __init__(self):
        """Initialize approval manager"""
        self.pending_approvals: Dict[str, ApprovalRequest] = {}
        self.policies: Dict[str, ApprovalPolicy] = {}
        self.callbacks: List[ApprovalCallback] = []
        self.approval_timeout = 300  # 5 minutes default
    
    def request_approval(
        self,
        command: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Request command execution approval
        
        Args:
            command: Command to execute
            context: Execution context
            
        Returns:
            Approval request ID
        """
        approval_id = secrets.token_urlsafe(16)
        
        request = ApprovalRequest(
            id=approval_id,
            command=command,
            context=context or {}
        )
        
        self.pending_approvals[approval_id] = request
        
        logger.info(f"Approval requested: {approval_id} for command: {command}")
        
        # TODO: Broadcast exec.approval.requested event
        
        return approval_id
    
    def approve(
        self,
        approval_id: str,
        approved_by: Optional[str] = None
    ) -> bool:
        """
        Approve command execution
        
        Args:
            approval_id: Approval request ID
            approved_by: User who approved
            
        Returns:
            True if successful
        """
        request = self.pending_approvals.get(approval_id)
        if not request:
            logger.warning(f"Approval request not found: {approval_id}")
            return False
        
        if request.status != "pending":
            logger.warning(f"Approval request already resolved: {approval_id}")
            return False
        
        request.status = "approved"
        request.approved_by = approved_by
        request.resolved_at = time.time()
        
        # Remove from pending
        del self.pending_approvals[approval_id]
        
        logger.info(f"Approval granted: {approval_id} by {approved_by}")
        
        # Trigger callbacks
        self._trigger_callbacks(request, True)
        
        # TODO: Broadcast exec.approval.resolved event
        
        return True
    
    def reject(
        self,
        approval_id: str,
        rejected_by: Optional[str] = None
    ) -> bool:
        """
        Reject command execution
        
        Args:
            approval_id: Approval request ID
            rejected_by: User who rejected
            
        Returns:
            True if successful
        """
        request = self.pending_approvals.get(approval_id)
        if not request:
            logger.warning(f"Approval request not found: {approval_id}")
            return False
        
        if request.status != "pending":
            logger.warning(f"Approval request already resolved: {approval_id}")
            return False
        
        request.status = "rejected"
        request.approved_by = rejected_by
        request.resolved_at = time.time()
        
        # Remove from pending
        del self.pending_approvals[approval_id]
        
        logger.info(f"Approval rejected: {approval_id} by {rejected_by}")
        
        # Trigger callbacks
        self._trigger_callbacks(request, False)
        
        # TODO: Broadcast exec.approval.resolved event
        
        return True
    
    def list_pending(self) -> List[Dict[str, Any]]:
        """
        List pending approval requests
        
        Returns:
            List of pending approvals
        """
        approvals = []
        for request in self.pending_approvals.values():
            approvals.append({
                "id": request.id,
                "command": request.command,
                "context": request.context,
                "requestedAt": request.requested_at,
                "status": request.status
            })
        return approvals
    
    def get_approval(self, approval_id: str) -> Optional[Dict[str, Any]]:
        """
        Get approval request details
        
        Args:
            approval_id: Approval request ID
            
        Returns:
            Approval details or None
        """
        request = self.pending_approvals.get(approval_id)
        if not request:
            return None
        
        return {
            "id": request.id,
            "command": request.command,
            "context": request.context,
            "requestedAt": request.requested_at,
            "status": request.status,
            "approvedBy": request.approved_by,
            "resolvedAt": request.resolved_at
        }
    
    def set_policy(self, policy_id: str, policy: ApprovalPolicy):
        """
        Set approval policy
        
        Args:
            policy_id: Policy identifier
            policy: Policy definition
        """
        self.policies[policy_id] = policy
        logger.info(f"Set approval policy: {policy_id}")
    
    def get_policy(self, policy_id: str) -> Optional[ApprovalPolicy]:
        """
        Get approval policy
        
        Args:
            policy_id: Policy identifier
            
        Returns:
            ApprovalPolicy or None
        """
        return self.policies.get(policy_id)
    
    def list_policies(self) -> List[Dict[str, Any]]:
        """
        List all approval policies
        
        Returns:
            List of policies
        """
        policies = []
        for policy_id, policy in self.policies.items():
            policies.append({
                "id": policy_id,
                "pattern": policy.pattern,
                "autoApprove": policy.auto_approve,
                "requireApproval": policy.require_approval,
                "allowedUsers": policy.allowed_users,
                "metadata": policy.metadata
            })
        return policies
    
    def register_callback(self, callback: ApprovalCallback):
        """
        Register callback for approval events
        
        Args:
            callback: Async callback function
        """
        self.callbacks.append(callback)
    
    def _trigger_callbacks(self, request: ApprovalRequest, approved: bool):
        """
        Trigger registered callbacks
        
        Args:
            request: Approval request
            approved: Whether approved or rejected
        """
        for callback in self.callbacks:
            try:
                # Schedule callback execution
                import asyncio
                asyncio.create_task(callback(request, approved))
            except Exception as e:
                logger.error(f"Callback error: {e}", exc_info=True)


# Global approval manager instance
_approval_manager: Optional[ExecApprovalManager] = None


def get_approval_manager() -> ExecApprovalManager:
    """Get global approval manager instance"""
    global _approval_manager
    if _approval_manager is None:
        _approval_manager = ExecApprovalManager()
    return _approval_manager


def set_approval_manager(manager: ExecApprovalManager):
    """Set global approval manager instance"""
    global _approval_manager
    _approval_manager = manager
