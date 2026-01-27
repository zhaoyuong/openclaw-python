"""Session tests"""

import pytest
from pathlib import Path
import tempfile
from clawdbot.agents.session import Session, SessionManager, Message


def test_message_creation():
    """Test message creation"""
    msg = Message(role="user", content="Hello")
    
    assert msg.role == "user"
    assert msg.content == "Hello"
    assert msg.timestamp is not None


def test_session_creation():
    """Test session creation"""
    with tempfile.TemporaryDirectory() as tmpdir:
        session = Session("test-session", Path(tmpdir))
        
        assert session.session_id == "test-session"
        assert len(session.messages) == 0


def test_session_add_message():
    """Test adding messages to session"""
    with tempfile.TemporaryDirectory() as tmpdir:
        session = Session("test-session", Path(tmpdir))
        
        session.add_user_message("Hello")
        session.add_assistant_message("Hi there!")
        
        assert len(session.messages) == 2
        assert session.messages[0].role == "user"
        assert session.messages[1].role == "assistant"


def test_session_persistence():
    """Test session persistence"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create and save messages
        session1 = Session("test-session", Path(tmpdir))
        session1.add_user_message("Test message")
        
        # Load in new session instance
        session2 = Session("test-session", Path(tmpdir))
        
        assert len(session2.messages) == 1
        assert session2.messages[0].content == "Test message"


def test_session_manager():
    """Test session manager"""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = SessionManager(Path(tmpdir))
        
        session1 = manager.get_session("session1")
        session2 = manager.get_session("session2")
        
        assert session1.session_id == "session1"
        assert session2.session_id == "session2"
        
        # Same session ID returns same instance
        session1_again = manager.get_session("session1")
        assert session1_again is session1
