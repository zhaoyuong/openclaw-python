"""
Tests for SessionEntry data model
"""

import pytest
from openclaw.agents.session_entry import (
    SessionEntry,
    SessionOrigin,
    DeliveryContext,
    merge_session_entry,
)


def test_session_entry_creation():
    """Test creating a SessionEntry"""
    entry = SessionEntry(
        session_id="test-123",
        updated_at=1000000,
    )
    
    assert entry.session_id == "test-123"
    assert entry.updated_at == 1000000
    assert entry.session_file is None
    assert entry.spawned_by is None


def test_session_entry_with_all_fields():
    """Test SessionEntry with all fields populated"""
    origin = SessionOrigin(
        label="test",
        provider="anthropic",
        chat_type="dm"
    )
    
    delivery = DeliveryContext(
        channel="telegram",
        to="user123"
    )
    
    entry = SessionEntry(
        session_id="test-456",
        updated_at=2000000,
        session_file="test-456.jsonl",
        spawned_by="parent-session",
        thinking_level="high",
        label="Test Session",
        origin=origin,
        delivery_context=delivery,
        input_tokens=100,
        output_tokens=200,
        total_tokens=300,
    )
    
    assert entry.session_id == "test-456"
    assert entry.thinking_level == "high"
    assert entry.label == "Test Session"
    assert entry.origin.provider == "anthropic"
    assert entry.delivery_context.channel == "telegram"
    assert entry.total_tokens == 300


def test_merge_session_entry_new():
    """Test merging into new entry"""
    patch = {
        "session_id": "new-123",
        "thinking_level": "medium",
        "label": "New Session",
    }
    
    result = merge_session_entry(None, patch)
    
    assert result.session_id == "new-123"
    assert result.thinking_level == "medium"
    assert result.label == "New Session"
    assert result.updated_at > 0


def test_merge_session_entry_existing():
    """Test merging into existing entry"""
    existing = SessionEntry(
        session_id="existing-123",
        updated_at=1000000,
        thinking_level="low",
        label="Old Label",
    )
    
    patch = {
        "thinking_level": "high",
        "input_tokens": 50,
    }
    
    result = merge_session_entry(existing, patch)
    
    assert result.session_id == "existing-123"
    assert result.thinking_level == "high"
    assert result.label == "Old Label"  # Preserved
    assert result.input_tokens == 50
    assert result.updated_at >= 1000000


def test_session_entry_model_dump():
    """Test converting SessionEntry to dict"""
    entry = SessionEntry(
        session_id="dump-test",
        updated_at=3000000,
        thinking_level="xhigh",
    )
    
    data = entry.model_dump(exclude_none=False)
    
    assert data["session_id"] == "dump-test"
    assert data["updated_at"] == 3000000
    assert data["thinking_level"] == "xhigh"
    assert "spawned_by" in data


def test_session_origin_with_alias():
    """Test SessionOrigin with 'from' field alias"""
    origin = SessionOrigin(
        **{"from": "user123", "to": "bot456"}
    )
    
    assert origin.from_ == "user123"
    assert origin.to == "bot456"


def test_delivery_context():
    """Test DeliveryContext"""
    delivery = DeliveryContext(
        channel="discord",
        to="channel123",
        account_id="account456",
        thread_id="thread789"
    )
    
    assert delivery.channel == "discord"
    assert delivery.to == "channel123"
    assert delivery.thread_id == "thread789"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
