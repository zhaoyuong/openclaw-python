"""Unit tests for security audit logging"""
import json
import pytest
from pathlib import Path
from tempfile import TemporaryDirectory

from openclaw.security.audit_extra import (
    AuditEvent,
    AuditLogger,
    get_audit_logger,
    read_audit_log,
)


class TestAuditEvent:
    """Test AuditEvent class"""
    
    def test_create_event(self):
        """Test creating audit event"""
        event = AuditEvent(
            event_type="command_execution",
            action="execute",
            resource="/bin/ls",
            result="success"
        )
        
        assert event.event_type == "command_execution"
        assert event.action == "execute"
        assert event.resource == "/bin/ls"
        assert event.result == "success"
        assert event.severity == "info"
    
    def test_event_to_dict(self):
        """Test converting event to dict"""
        event = AuditEvent(
            event_type="file_access",
            action="read",
            resource="/etc/passwd",
            result="blocked"
        )
        
        data = event.to_dict()
        
        assert isinstance(data, dict)
        assert data["event_type"] == "file_access"
        assert data["action"] == "read"
        assert data["result"] == "blocked"
    
    def test_event_with_details(self):
        """Test event with details"""
        event = AuditEvent(
            event_type="api_call",
            action="call",
            resource="openai/gpt-4",
            result="success",
            details={"tokens": 100}
        )
        
        assert event.details["tokens"] == 100


class TestAuditLogger:
    """Test AuditLogger class"""
    
    def test_create_logger_without_file(self):
        """Test creating logger without file"""
        logger = AuditLogger()
        assert logger is not None
        assert logger.audit_file is None
    
    def test_create_logger_with_file(self):
        """Test creating logger with file"""
        with TemporaryDirectory() as tmpdir:
            audit_file = Path(tmpdir) / "audit.log"
            logger = AuditLogger(audit_file=audit_file)
            
            assert logger.audit_file == audit_file
    
    def test_log_event(self):
        """Test logging event"""
        with TemporaryDirectory() as tmpdir:
            audit_file = Path(tmpdir) / "audit.log"
            logger = AuditLogger(audit_file=audit_file)
            
            event = AuditEvent(
                event_type="test",
                action="test",
                resource="test",
                result="success"
            )
            
            logger.log_event(event)
            
            # Check file was created and written
            assert audit_file.exists()
            
            # Read and verify
            with open(audit_file) as f:
                line = f.readline()
                data = json.loads(line)
                assert data["event_type"] == "test"
    
    def test_log_command_execution(self):
        """Test logging command execution"""
        with TemporaryDirectory() as tmpdir:
            audit_file = Path(tmpdir) / "audit.log"
            logger = AuditLogger(audit_file=audit_file)
            
            logger.log_command_execution(
                command="ls -la",
                user_id="user1",
                session_id="session1",
                result="success",
                exit_code=0
            )
            
            # Verify log entry
            with open(audit_file) as f:
                line = f.readline()
                data = json.loads(line)
                assert data["event_type"] == "command_execution"
                assert data["resource"] == "ls -la"
                assert data["details"]["exit_code"] == 0
    
    def test_log_file_access(self):
        """Test logging file access"""
        with TemporaryDirectory() as tmpdir:
            audit_file = Path(tmpdir) / "audit.log"
            logger = AuditLogger(audit_file=audit_file)
            
            logger.log_file_access(
                file_path="/tmp/test.txt",
                operation="read",
                user_id="user1",
                result="success"
            )
            
            with open(audit_file) as f:
                line = f.readline()
                data = json.loads(line)
                assert data["event_type"] == "file_access"
                assert data["action"] == "read"
    
    def test_log_policy_violation(self):
        """Test logging policy violation"""
        with TemporaryDirectory() as tmpdir:
            audit_file = Path(tmpdir) / "audit.log"
            logger = AuditLogger(audit_file=audit_file)
            
            logger.log_policy_violation(
                policy="file_write",
                action="write",
                resource="/etc/passwd",
                reason="Access denied"
            )
            
            with open(audit_file) as f:
                line = f.readline()
                data = json.loads(line)
                assert data["event_type"] == "policy_violation"
                assert data["result"] == "blocked"
                assert data["severity"] == "warning"
    
    def test_log_multiple_events(self):
        """Test logging multiple events"""
        with TemporaryDirectory() as tmpdir:
            audit_file = Path(tmpdir) / "audit.log"
            logger = AuditLogger(audit_file=audit_file)
            
            for i in range(5):
                event = AuditEvent(
                    event_type="test",
                    action=f"action_{i}",
                    resource=f"resource_{i}",
                    result="success"
                )
                logger.log_event(event)
            
            # Read all lines
            with open(audit_file) as f:
                lines = f.readlines()
            
            assert len(lines) == 5


class TestReadAuditLog:
    """Test reading audit log"""
    
    def test_read_empty_log(self):
        """Test reading empty log"""
        with TemporaryDirectory() as tmpdir:
            audit_file = Path(tmpdir) / "audit.log"
            audit_file.touch()
            
            events = read_audit_log(audit_file)
            assert len(events) == 0
    
    def test_read_log_with_events(self):
        """Test reading log with events"""
        with TemporaryDirectory() as tmpdir:
            audit_file = Path(tmpdir) / "audit.log"
            logger = AuditLogger(audit_file=audit_file)
            
            # Write some events
            for i in range(3):
                event = AuditEvent(
                    event_type="test",
                    action=f"action_{i}",
                    resource=f"resource_{i}",
                    result="success"
                )
                logger.log_event(event)
            
            # Read events
            events = read_audit_log(audit_file)
            
            assert len(events) == 3
            assert events[0].action == "action_0"
            assert events[1].action == "action_1"
            assert events[2].action == "action_2"
    
    def test_read_with_limit(self):
        """Test reading with limit"""
        with TemporaryDirectory() as tmpdir:
            audit_file = Path(tmpdir) / "audit.log"
            logger = AuditLogger(audit_file=audit_file)
            
            # Write 10 events
            for i in range(10):
                event = AuditEvent(
                    event_type="test",
                    action=f"action_{i}",
                    resource=f"resource_{i}",
                    result="success"
                )
                logger.log_event(event)
            
            # Read with limit
            events = read_audit_log(audit_file, limit=5)
            
            assert len(events) == 5
    
    def test_read_with_event_type_filter(self):
        """Test reading with event type filter"""
        with TemporaryDirectory() as tmpdir:
            audit_file = Path(tmpdir) / "audit.log"
            logger = AuditLogger(audit_file=audit_file)
            
            # Write different event types
            logger.log_command_execution("ls", result="success")
            logger.log_file_access("/tmp/test", "read", result="success")
            logger.log_command_execution("pwd", result="success")
            
            # Read only command_execution events
            events = read_audit_log(audit_file, event_type="command_execution")
            
            assert len(events) == 2
            assert all(e.event_type == "command_execution" for e in events)
    
    def test_read_with_severity_filter(self):
        """Test reading with severity filter"""
        with TemporaryDirectory() as tmpdir:
            audit_file = Path(tmpdir) / "audit.log"
            logger = AuditLogger(audit_file=audit_file)
            
            # Write events with different severities
            event1 = AuditEvent(
                event_type="test",
                action="action1",
                resource="res1",
                result="success",
                severity="info"
            )
            logger.log_event(event1)
            
            event2 = AuditEvent(
                event_type="test",
                action="action2",
                resource="res2",
                result="blocked",
                severity="warning"
            )
            logger.log_event(event2)
            
            # Read only warnings
            events = read_audit_log(audit_file, severity="warning")
            
            assert len(events) == 1
            assert events[0].severity == "warning"


def test_get_audit_logger():
    """Test getting global audit logger"""
    logger = get_audit_logger()
    assert logger is not None
    
    # Should return same instance
    logger2 = get_audit_logger()
    assert logger is logger2
