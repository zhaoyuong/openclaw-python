"""Unit tests for unified event system"""

import pytest
from openclaw.events import Event, EventType, EventBus, get_event_bus, reset_event_bus


class TestEvent:
    """Test Event class"""
    
    def test_create_event(self):
        """Test event creation"""
        event = Event(
            type=EventType.AGENT_TEXT,
            source="test-agent",
            data={"text": "Hello"}
        )
        
        assert event.type == EventType.AGENT_TEXT
        assert event.source == "test-agent"
        assert event.data["text"] == "Hello"
    
    def test_event_to_dict(self):
        """Test event serialization"""
        event = Event(
            type=EventType.AGENT_TEXT,
            source="test",
            session_id="sess-1",
            data={"text": "Hi"}
        )
        
        d = event.to_dict()
        assert d["type"] == "agent.text"
        assert d["source"] == "test"
        assert d["session_id"] == "sess-1"
    
    def test_event_from_dict(self):
        """Test event deserialization"""
        data = {
            "type": "agent.text",
            "source": "test",
            "data": {"text": "Hello"},
            "timestamp": "2026-02-01T00:00:00"
        }
        
        event = Event.from_dict(data)
        assert event.type == EventType.AGENT_TEXT
        assert event.source == "test"


class TestEventBus:
    """Test EventBus"""
    
    def setup_method(self):
        """Reset event bus before each test"""
        reset_event_bus()
    
    @pytest.mark.asyncio
    async def test_subscribe_and_publish(self):
        """Test basic pub/sub"""
        bus = get_event_bus()
        received = []
        
        async def handler(event):
            received.append(event.type)
        
        bus.subscribe(EventType.AGENT_TEXT, handler)
        
        await bus.publish(Event(
            type=EventType.AGENT_TEXT,
            source="test",
            data={}
        ))
        
        assert len(received) == 1
        assert received[0] == EventType.AGENT_TEXT
    
    @pytest.mark.asyncio
    async def test_multiple_subscribers(self):
        """Test multiple subscribers for same event"""
        bus = get_event_bus()
        counts = {"a": 0, "b": 0, "c": 0}
        
        async def handler_a(event):
            counts["a"] += 1
        
        async def handler_b(event):
            counts["b"] += 1
        
        async def handler_c(event):
            counts["c"] += 1
        
        bus.subscribe(EventType.AGENT_TEXT, handler_a)
        bus.subscribe(EventType.AGENT_TEXT, handler_b)
        bus.subscribe(EventType.AGENT_TEXT, handler_c)
        
        await bus.publish(Event(
            type=EventType.AGENT_TEXT,
            source="test",
            data={}
        ))
        
        assert counts["a"] == 1
        assert counts["b"] == 1
        assert counts["c"] == 1
    
    @pytest.mark.asyncio
    async def test_wildcard_subscription(self):
        """Test wildcard subscription (all events)"""
        bus = get_event_bus()
        received = []
        
        async def wildcard_handler(event):
            received.append(event.type)
        
        bus.subscribe(None, wildcard_handler)
        
        await bus.publish(Event(type=EventType.AGENT_TEXT, source="test", data={}))
        await bus.publish(Event(type=EventType.AGENT_THINKING, source="test", data={}))
        await bus.publish(Event(type=EventType.CHANNEL_STARTED, source="test", data={}))
        
        assert len(received) == 3
    
    @pytest.mark.asyncio
    async def test_unsubscribe(self):
        """Test unsubscribing"""
        bus = get_event_bus()
        received = []
        
        async def handler(event):
            received.append(event)
        
        bus.subscribe(EventType.AGENT_TEXT, handler)
        
        await bus.publish(Event(type=EventType.AGENT_TEXT, source="test", data={}))
        assert len(received) == 1
        
        # Unsubscribe
        result = bus.unsubscribe(EventType.AGENT_TEXT, handler)
        assert result is True
        
        await bus.publish(Event(type=EventType.AGENT_TEXT, source="test", data={}))
        assert len(received) == 1  # Should not increase
    
    @pytest.mark.asyncio
    async def test_error_handling(self):
        """Test that errors in listeners don't crash bus"""
        bus = get_event_bus()
        healthy_called = []
        
        async def buggy_handler(event):
            raise Exception("Oops!")
        
        async def healthy_handler(event):
            healthy_called.append(True)
        
        bus.subscribe(EventType.AGENT_TEXT, buggy_handler)
        bus.subscribe(EventType.AGENT_TEXT, healthy_handler)
        
        # Should not raise
        await bus.publish(Event(type=EventType.AGENT_TEXT, source="test", data={}))
        
        # Healthy handler should still be called
        assert len(healthy_called) == 1
    
    def test_get_stats(self):
        """Test event bus statistics"""
        bus = get_event_bus()
        
        async def handler(event):
            pass
        
        bus.subscribe(EventType.AGENT_TEXT, handler)
        bus.subscribe(EventType.CHANNEL_STARTED, handler)
        
        stats = bus.get_stats()
        assert stats["name"] == "global"
        assert stats["total_listeners"] >= 2
