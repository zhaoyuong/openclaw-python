"""Execution approval system for sensitive operations

This module provides an approval system for operations that require
user confirmation before execution, such as destructive file operations,
sensitive command execution, or external API calls.
"""
from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any, Callable

logger = logging.getLogger(__name__)


class ApprovalStatus(Enum):
    """Approval status"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


@dataclass
class ApprovalRequest:
    """Approval request"""
    
    id: str
    operation: str
    description: str
    severity: str = "medium"  # low, medium, high, critical
    context: dict[str, Any] = field(default_factory=dict)
    status: ApprovalStatus = ApprovalStatus.PENDING
    requested_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    decided_at: str | None = None
    decided_by: str | None = None
    reason: str | None = None
    timeout_seconds: int = 300  # 5 minutes default
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "operation": self.operation,
            "description": self.description,
            "severity": self.severity,
            "context": self.context,
            "status": self.status.value,
            "requested_at": self.requested_at,
            "decided_at": self.decided_at,
            "decided_by": self.decided_by,
            "reason": self.reason,
            "timeout_seconds": self.timeout_seconds,
        }


class ApprovalManager:
    """Manager for execution approvals"""
    
    def __init__(self):
        """Initialize approval manager"""
        self.pending_approvals: dict[str, ApprovalRequest] = {}
        self.approval_history: list[ApprovalRequest] = []
        self.approval_handlers: list[Callable] = []
        self.auto_approve_operations: set[str] = set()
        self.auto_reject_operations: set[str] = set()
    
    def register_handler(self, handler: Callable[[ApprovalRequest], None]) -> None:
        """
        Register approval handler
        
        Args:
            handler: Handler function to call when approval is needed
        """
        self.approval_handlers.append(handler)
    
    def set_auto_approve(self, operation: str) -> None:
        """
        Set operation to auto-approve
        
        Args:
            operation: Operation name
        """
        self.auto_approve_operations.add(operation)
        if operation in self.auto_reject_operations:
            self.auto_reject_operations.remove(operation)
    
    def set_auto_reject(self, operation: str) -> None:
        """
        Set operation to auto-reject
        
        Args:
            operation: Operation name
        """
        self.auto_reject_operations.add(operation)
        if operation in self.auto_approve_operations:
            self.auto_approve_operations.remove(operation)
    
    async def request_approval(
        self,
        operation: str,
        description: str,
        severity: str = "medium",
        context: dict[str, Any] | None = None,
        timeout_seconds: int = 300,
    ) -> bool:
        """
        Request approval for operation
        
        Args:
            operation: Operation name
            description: Human-readable description
            severity: Severity level (low, medium, high, critical)
            context: Additional context
            timeout_seconds: Timeout in seconds
            
        Returns:
            True if approved, False if rejected
        """
        # Check auto-approve
        if operation in self.auto_approve_operations:
            logger.info(f"Auto-approved operation: {operation}")
            return True
        
        # Check auto-reject
        if operation in self.auto_reject_operations:
            logger.warning(f"Auto-rejected operation: {operation}")
            return False
        
        # Create approval request
        import uuid
        request_id = str(uuid.uuid4())
        
        request = ApprovalRequest(
            id=request_id,
            operation=operation,
            description=description,
            severity=severity,
            context=context or {},
            timeout_seconds=timeout_seconds,
        )
        
        self.pending_approvals[request_id] = request
        
        # Notify handlers
        for handler in self.approval_handlers:
            try:
                handler(request)
            except Exception as e:
                logger.error(f"Approval handler error: {e}")
        
        # Wait for decision with timeout
        try:
            result = await asyncio.wait_for(
                self._wait_for_decision(request_id),
                timeout=timeout_seconds
            )
            
            return result
            
        except asyncio.TimeoutError:
            # Timeout - mark as expired
            request.status = ApprovalStatus.EXPIRED
            request.decided_at = datetime.now(UTC).isoformat()
            self.approval_history.append(request)
            del self.pending_approvals[request_id]
            
            logger.warning(f"Approval request timeout: {operation}")
            return False
    
    async def _wait_for_decision(self, request_id: str) -> bool:
        """
        Wait for decision on approval request
        
        Args:
            request_id: Request ID
            
        Returns:
            True if approved
        """
        while request_id in self.pending_approvals:
            request = self.pending_approvals[request_id]
            
            if request.status == ApprovalStatus.APPROVED:
                return True
            elif request.status in (ApprovalStatus.REJECTED, ApprovalStatus.CANCELLED):
                return False
            
            await asyncio.sleep(0.1)
        
        return False
    
    def approve(
        self,
        request_id: str,
        decided_by: str | None = None,
        reason: str | None = None,
    ) -> bool:
        """
        Approve a request
        
        Args:
            request_id: Request ID
            decided_by: Who approved it
            reason: Approval reason
            
        Returns:
            True if approved successfully
        """
        if request_id not in self.pending_approvals:
            logger.warning(f"Approval request not found: {request_id}")
            return False
        
        request = self.pending_approvals[request_id]
        request.status = ApprovalStatus.APPROVED
        request.decided_at = datetime.now(UTC).isoformat()
        request.decided_by = decided_by
        request.reason = reason
        
        # Move to history
        self.approval_history.append(request)
        del self.pending_approvals[request_id]
        
        logger.info(f"Approval granted: {request.operation} by {decided_by}")
        return True
    
    def reject(
        self,
        request_id: str,
        decided_by: str | None = None,
        reason: str | None = None,
    ) -> bool:
        """
        Reject a request
        
        Args:
            request_id: Request ID
            decided_by: Who rejected it
            reason: Rejection reason
            
        Returns:
            True if rejected successfully
        """
        if request_id not in self.pending_approvals:
            logger.warning(f"Approval request not found: {request_id}")
            return False
        
        request = self.pending_approvals[request_id]
        request.status = ApprovalStatus.REJECTED
        request.decided_at = datetime.now(UTC).isoformat()
        request.decided_by = decided_by
        request.reason = reason
        
        # Move to history
        self.approval_history.append(request)
        del self.pending_approvals[request_id]
        
        logger.warning(f"Approval rejected: {request.operation} by {decided_by}")
        return True
    
    def cancel(self, request_id: str) -> bool:
        """
        Cancel a request
        
        Args:
            request_id: Request ID
            
        Returns:
            True if cancelled successfully
        """
        if request_id not in self.pending_approvals:
            return False
        
        request = self.pending_approvals[request_id]
        request.status = ApprovalStatus.CANCELLED
        request.decided_at = datetime.now(UTC).isoformat()
        
        self.approval_history.append(request)
        del self.pending_approvals[request_id]
        
        logger.info(f"Approval cancelled: {request.operation}")
        return True
    
    def get_pending(self) -> list[ApprovalRequest]:
        """
        Get all pending approval requests
        
        Returns:
            List of pending requests
        """
        return list(self.pending_approvals.values())
    
    def get_history(self, limit: int | None = None) -> list[ApprovalRequest]:
        """
        Get approval history
        
        Args:
            limit: Maximum number of items to return
            
        Returns:
            List of historical requests
        """
        if limit:
            return self.approval_history[-limit:]
        return self.approval_history.copy()
    
    def clear_history(self) -> None:
        """Clear approval history"""
        self.approval_history.clear()


# Global approval manager
_approval_manager: ApprovalManager | None = None


def get_approval_manager() -> ApprovalManager:
    """
    Get global approval manager
    
    Returns:
        Global approval manager instance
    """
    global _approval_manager
    
    if _approval_manager is None:
        _approval_manager = ApprovalManager()
    
    return _approval_manager


async def require_approval(
    operation: str,
    description: str,
    severity: str = "medium",
    **context
) -> bool:
    """
    Require approval for operation (convenience function)
    
    Args:
        operation: Operation name
        description: Description
        severity: Severity level
        **context: Additional context
        
    Returns:
        True if approved
    """
    manager = get_approval_manager()
    return await manager.request_approval(
        operation=operation,
        description=description,
        severity=severity,
        context=context
    )
