"""Filesystem audit logging

This module provides filesystem-specific audit logging including:
- File read/write/delete operations
- Directory operations
- Permission changes
- File security events
"""
from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .audit_extra import AuditLogger, get_audit_logger

logger = logging.getLogger(__name__)


@dataclass
class FileAuditEvent:
    """Filesystem audit event"""
    
    operation: str  # read, write, delete, chmod, mkdir, rmdir
    path: str
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    user_id: str | None = None
    session_id: str | None = None
    result: str = "success"
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary"""
        return {
            "operation": self.operation,
            "path": self.path,
            "timestamp": self.timestamp,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "result": self.result,
            "error": self.error,
            "metadata": self.metadata,
        }


class FilesystemAuditor:
    """Filesystem operations auditor"""
    
    def __init__(self, audit_logger: AuditLogger | None = None):
        """
        Initialize filesystem auditor
        
        Args:
            audit_logger: Audit logger to use
        """
        self.audit_logger = audit_logger or get_audit_logger()
    
    def audit_read(
        self,
        path: str | Path,
        user_id: str | None = None,
        session_id: str | None = None,
        result: str = "success",
        error: str | None = None,
        bytes_read: int | None = None,
    ) -> None:
        """
        Audit file read operation
        
        Args:
            path: File path
            user_id: User ID
            session_id: Session ID
            result: Operation result
            error: Error message if failed
            bytes_read: Number of bytes read
        """
        event = FileAuditEvent(
            operation="read",
            path=str(path),
            user_id=user_id,
            session_id=session_id,
            result=result,
            error=error,
            metadata={"bytes_read": bytes_read} if bytes_read is not None else {}
        )
        
        self.audit_logger.log_file_access(
            file_path=str(path),
            operation="read",
            user_id=user_id,
            session_id=session_id,
            result=result
        )
    
    def audit_write(
        self,
        path: str | Path,
        user_id: str | None = None,
        session_id: str | None = None,
        result: str = "success",
        error: str | None = None,
        bytes_written: int | None = None,
        created: bool = False,
    ) -> None:
        """
        Audit file write operation
        
        Args:
            path: File path
            user_id: User ID
            session_id: Session ID
            result: Operation result
            error: Error message if failed
            bytes_written: Number of bytes written
            created: Whether file was created
        """
        event = FileAuditEvent(
            operation="write",
            path=str(path),
            user_id=user_id,
            session_id=session_id,
            result=result,
            error=error,
            metadata={
                "bytes_written": bytes_written,
                "created": created
            }
        )
        
        self.audit_logger.log_file_access(
            file_path=str(path),
            operation="write" if not created else "create",
            user_id=user_id,
            session_id=session_id,
            result=result
        )
    
    def audit_delete(
        self,
        path: str | Path,
        user_id: str | None = None,
        session_id: str | None = None,
        result: str = "success",
        error: str | None = None,
        is_directory: bool = False,
    ) -> None:
        """
        Audit file/directory deletion
        
        Args:
            path: Path to deleted item
            user_id: User ID
            session_id: Session ID
            result: Operation result
            error: Error message if failed
            is_directory: Whether deleted item was a directory
        """
        event = FileAuditEvent(
            operation="delete" if not is_directory else "rmdir",
            path=str(path),
            user_id=user_id,
            session_id=session_id,
            result=result,
            error=error,
            metadata={"is_directory": is_directory}
        )
        
        self.audit_logger.log_file_access(
            file_path=str(path),
            operation="delete",
            user_id=user_id,
            session_id=session_id,
            result=result
        )
    
    def audit_chmod(
        self,
        path: str | Path,
        old_mode: int,
        new_mode: int,
        user_id: str | None = None,
        session_id: str | None = None,
        result: str = "success",
        error: str | None = None,
    ) -> None:
        """
        Audit permission change
        
        Args:
            path: File path
            old_mode: Old file mode
            new_mode: New file mode
            user_id: User ID
            session_id: Session ID
            result: Operation result
            error: Error message if failed
        """
        event = FileAuditEvent(
            operation="chmod",
            path=str(path),
            user_id=user_id,
            session_id=session_id,
            result=result,
            error=error,
            metadata={
                "old_mode": oct(old_mode),
                "new_mode": oct(new_mode)
            }
        )
        
        self.audit_logger.log_file_access(
            file_path=str(path),
            operation="chmod",
            user_id=user_id,
            session_id=session_id,
            result=result
        )
    
    def audit_mkdir(
        self,
        path: str | Path,
        user_id: str | None = None,
        session_id: str | None = None,
        result: str = "success",
        error: str | None = None,
        mode: int | None = None,
    ) -> None:
        """
        Audit directory creation
        
        Args:
            path: Directory path
            user_id: User ID
            session_id: Session ID
            result: Operation result
            error: Error message if failed
            mode: Directory mode
        """
        event = FileAuditEvent(
            operation="mkdir",
            path=str(path),
            user_id=user_id,
            session_id=session_id,
            result=result,
            error=error,
            metadata={"mode": oct(mode)} if mode is not None else {}
        )
        
        self.audit_logger.log_file_access(
            file_path=str(path),
            operation="mkdir",
            user_id=user_id,
            session_id=session_id,
            result=result
        )
    
    def check_sensitive_file(self, path: str | Path) -> bool:
        """
        Check if file is sensitive (e.g., contains credentials)
        
        Args:
            path: File path
            
        Returns:
            True if file is sensitive
        """
        path_str = str(path).lower()
        
        sensitive_patterns = [
            ".env",
            "secret",
            "credential",
            "password",
            "api_key",
            "apikey",
            "token",
            "private_key",
            "id_rsa",
            ".pem",
            ".key",
        ]
        
        return any(pattern in path_str for pattern in sensitive_patterns)
    
    def check_path_traversal(self, path: str | Path, base_path: str | Path) -> bool:
        """
        Check if path attempts directory traversal outside base path
        
        Args:
            path: Path to check
            base_path: Allowed base path
            
        Returns:
            True if path is safe
        """
        try:
            path_resolved = Path(path).resolve()
            base_resolved = Path(base_path).resolve()
            
            # Check if resolved path is within base path
            return path_resolved.is_relative_to(base_resolved)
            
        except Exception:
            return False


# Global filesystem auditor instance
_fs_auditor: FilesystemAuditor | None = None


def get_fs_auditor() -> FilesystemAuditor:
    """
    Get global filesystem auditor
    
    Returns:
        Global filesystem auditor
    """
    global _fs_auditor
    
    if _fs_auditor is None:
        _fs_auditor = FilesystemAuditor()
    
    return _fs_auditor
