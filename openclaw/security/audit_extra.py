"""Extended audit logging for security events

This module provides additional audit logging capabilities beyond basic
security auditing, including detailed event tracking and compliance logging.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class AuditEvent:
    """Security audit event"""
    
    event_type: str
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    user_id: str | None = None
    session_id: str | None = None
    channel: str | None = None
    action: str = ""
    resource: str = ""
    result: str = "unknown"  # success, failure, blocked
    details: dict[str, Any] = field(default_factory=dict)
    severity: str = "info"  # info, warning, critical
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary"""
        return {
            "event_type": self.event_type,
            "timestamp": self.timestamp,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "channel": self.channel,
            "action": self.action,
            "resource": self.resource,
            "result": self.result,
            "details": self.details,
            "severity": self.severity,
        }


class AuditLogger:
    """Extended audit logger"""
    
    def __init__(self, audit_file: Path | None = None):
        """
        Initialize audit logger
        
        Args:
            audit_file: Path to audit log file (JSON Lines format)
        """
        self.audit_file = audit_file
        
        if self.audit_file:
            self.audit_file.parent.mkdir(parents=True, exist_ok=True)
    
    def log_event(self, event: AuditEvent) -> None:
        """
        Log audit event
        
        Args:
            event: Audit event to log
        """
        # Log to Python logger
        log_msg = (
            f"AUDIT: {event.event_type} - {event.action} on {event.resource} "
            f"[{event.result}]"
        )
        
        if event.severity == "critical":
            logger.critical(log_msg)
        elif event.severity == "warning":
            logger.warning(log_msg)
        else:
            logger.info(log_msg)
        
        # Write to audit file
        if self.audit_file:
            try:
                with open(self.audit_file, "a") as f:
                    f.write(json.dumps(event.to_dict()) + "\n")
            except Exception as e:
                logger.error(f"Failed to write audit log: {e}")
    
    def log_command_execution(
        self,
        command: str,
        user_id: str | None = None,
        session_id: str | None = None,
        result: str = "success",
        exit_code: int | None = None,
    ) -> None:
        """
        Log command execution
        
        Args:
            command: Command that was executed
            user_id: User ID
            session_id: Session ID
            result: Execution result
            exit_code: Command exit code
        """
        event = AuditEvent(
            event_type="command_execution",
            user_id=user_id,
            session_id=session_id,
            action="execute",
            resource=command,
            result=result,
            details={"exit_code": exit_code} if exit_code is not None else {},
            severity="info" if result == "success" else "warning"
        )
        self.log_event(event)
    
    def log_file_access(
        self,
        file_path: str,
        operation: str,  # read, write, delete
        user_id: str | None = None,
        session_id: str | None = None,
        result: str = "success",
    ) -> None:
        """
        Log file access
        
        Args:
            file_path: Path to accessed file
            operation: Type of operation
            user_id: User ID
            session_id: Session ID
            result: Operation result
        """
        event = AuditEvent(
            event_type="file_access",
            user_id=user_id,
            session_id=session_id,
            action=operation,
            resource=file_path,
            result=result,
            severity="info"
        )
        self.log_event(event)
    
    def log_api_call(
        self,
        api_key: str,
        provider: str,
        model: str,
        tokens: int | None = None,
        user_id: str | None = None,
        session_id: str | None = None,
        result: str = "success",
    ) -> None:
        """
        Log API call
        
        Args:
            api_key: API key used (last 4 chars)
            provider: Provider name
            model: Model name
            tokens: Token count
            user_id: User ID
            session_id: Session ID
            result: Call result
        """
        event = AuditEvent(
            event_type="api_call",
            user_id=user_id,
            session_id=session_id,
            action="call",
            resource=f"{provider}/{model}",
            result=result,
            details={
                "api_key_suffix": api_key[-4:] if len(api_key) >= 4 else "****",
                "tokens": tokens
            },
            severity="info"
        )
        self.log_event(event)
    
    def log_policy_violation(
        self,
        policy: str,
        action: str,
        resource: str,
        user_id: str | None = None,
        session_id: str | None = None,
        reason: str = "",
    ) -> None:
        """
        Log policy violation
        
        Args:
            policy: Policy that was violated
            action: Attempted action
            resource: Target resource
            user_id: User ID
            session_id: Session ID
            reason: Violation reason
        """
        event = AuditEvent(
            event_type="policy_violation",
            user_id=user_id,
            session_id=session_id,
            action=action,
            resource=resource,
            result="blocked",
            details={"policy": policy, "reason": reason},
            severity="warning"
        )
        self.log_event(event)
    
    def log_auth_attempt(
        self,
        user_id: str,
        channel: str | None = None,
        result: str = "success",
        ip_address: str | None = None,
    ) -> None:
        """
        Log authentication attempt
        
        Args:
            user_id: User ID attempting auth
            channel: Channel name
            result: Auth result
            ip_address: IP address
        """
        event = AuditEvent(
            event_type="auth_attempt",
            user_id=user_id,
            channel=channel,
            action="authenticate",
            resource="auth_system",
            result=result,
            details={"ip_address": ip_address} if ip_address else {},
            severity="warning" if result != "success" else "info"
        )
        self.log_event(event)


# Global audit logger instance
_audit_logger: AuditLogger | None = None


def get_audit_logger(audit_file: Path | None = None) -> AuditLogger:
    """
    Get global audit logger instance
    
    Args:
        audit_file: Audit file path (only used on first call)
        
    Returns:
        Global audit logger
    """
    global _audit_logger
    
    if _audit_logger is None:
        _audit_logger = AuditLogger(audit_file=audit_file)
    
    return _audit_logger


def read_audit_log(
    audit_file: Path,
    limit: int | None = None,
    event_type: str | None = None,
    severity: str | None = None,
) -> list[AuditEvent]:
    """
    Read audit log entries
    
    Args:
        audit_file: Path to audit log file
        limit: Maximum entries to return
        event_type: Filter by event type
        severity: Filter by severity
        
    Returns:
        List of audit events
    """
    events: list[AuditEvent] = []
    
    if not audit_file.exists():
        return events
    
    try:
        with open(audit_file, "r") as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    
                    # Apply filters
                    if event_type and data.get("event_type") != event_type:
                        continue
                    if severity and data.get("severity") != severity:
                        continue
                    
                    event = AuditEvent(**data)
                    events.append(event)
                    
                    if limit and len(events) >= limit:
                        break
                        
                except json.JSONDecodeError:
                    continue
                    
    except Exception as e:
        logger.error(f"Failed to read audit log: {e}")
    
    return events
