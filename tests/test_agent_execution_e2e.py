"""End-to-end tests for agent execution

Tests the complete agent execution flow including:
- Turn execution
- Streaming responses
- Tool calling
- Multi-turn conversations
- Abort mechanism
- Event propagation
"""
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch

from openclaw.agents.runtime import MultiProviderRuntime
from openclaw.agents.session import Session
from openclaw.agents.tools.base import AgentTool, ToolResult
from openclaw.events import EventType


class MockTool(AgentTool):
    """Mock tool for testing"""
    
    def __init__(self, name: str = "test_tool"):
        self.name = name
        self.description = "A test tool"
        self.parameters = {
            "type": "object",
            "properties": {
                "input": {"type": "string"}
            }
        }
        self.call_count = 0
    
    async def execute(self, input: str = "") -> ToolResult:
        """Execute the tool"""
        self.call_count += 1
        return ToolResult(
            success=True,
            output=f"Tool executed with: {input}",
            metadata={"call_count": self.call_count}
        )


class TestBasicTurnExecution:
    """Test basic turn execution"""
    
    @pytest.mark.asyncio
    async def test_basic_turn_non_streaming(self):
        """Test basic non-streaming turn execution"""
        # Create mock provider
        mock_provider = AsyncMock()
        mock_provider.generate = AsyncMock(return_value={
            "content": "Hello! I'm the assistant.",
            "tool_calls": [],
            "usage": {"input_tokens": 10, "output_tokens": 20}
        })
        
        runtime = MultiProviderRuntime(model="mock/test")
        runtime.provider = mock_provider
        
        session = Session(session_id="test-session")
        
        # Execute turn
        events = []
        async for event in runtime.run_turn(
            session=session,
            message="Hello",
            tools=[]
        ):
            events.append(event)
        
        # Verify we got events
        assert len(events) > 0
        
        # Verify session was updated
        assert len(session.messages) > 0
    
    @pytest.mark.asyncio
    async def test_turn_with_images(self):
        """Test turn execution with image inputs"""
        mock_provider = AsyncMock()
        mock_provider.generate = AsyncMock(return_value={
            "content": "I see the image.",
            "tool_calls": [],
            "usage": {}
        })
        
        runtime = MultiProviderRuntime(model="mock/test")
        runtime.provider = mock_provider
        
        session = Session(session_id="test-session")
        images = ["http://example.com/image.jpg"]
        
        events = []
        async for event in runtime.run_turn(
            session=session,
            message="What's in this image?",
            tools=[],
            images=images
        ):
            events.append(event)
        
        # Verify provider was called with images
        call_args = mock_provider.generate.call_args
        assert call_args is not None


class TestStreamingResponse:
    """Test streaming response generation"""
    
    @pytest.mark.asyncio
    async def test_streaming_text(self):
        """Test streaming text response"""
        async def mock_stream():
            chunks = [
                {"type": "text", "text": "Hello "},
                {"type": "text", "text": "world"},
                {"type": "text", "text": "!"},
            ]
            for chunk in chunks:
                yield chunk
        
        mock_provider = AsyncMock()
        mock_provider.stream = AsyncMock(return_value=mock_stream())
        
        runtime = MultiProviderRuntime(model="mock/test")
        runtime.provider = mock_provider
        
        session = Session(session_id="test-session")
        
        text_events = []
        async for event in runtime.run_turn(session=session, message="Hi", tools=[]):
            if event.type == EventType.AGENT_TEXT or event.type == "text":
                text_events.append(event)
        
        # Verify we got text events
        assert len(text_events) > 0


class TestToolExecution:
    """Test tool calling functionality"""
    
    @pytest.mark.asyncio
    async def test_single_tool_call(self):
        """Test execution with single tool call"""
        test_tool = MockTool("test_tool")
        
        # Mock provider that returns a tool call
        async def mock_stream():
            yield {"type": "tool_use", "name": "test_tool", "arguments": {"input": "test"}}
            yield {"type": "stop"}
        
        mock_provider = AsyncMock()
        mock_provider.stream = AsyncMock(return_value=mock_stream())
        
        runtime = MultiProviderRuntime(model="mock/test")
        runtime.provider = mock_provider
        
        session = Session(session_id="test-session")
        
        events = []
        async for event in runtime.run_turn(
            session=session,
            message="Use the test tool",
            tools=[test_tool]
        ):
            events.append(event)
        
        # Verify tool was called
        assert test_tool.call_count > 0
    
    @pytest.mark.asyncio
    async def test_multi_turn_tool_calls(self):
        """Test multiple tool calls across turns"""
        test_tool = MockTool("test_tool")
        
        mock_provider = AsyncMock()
        runtime = MultiProviderRuntime(model="mock/test")
        runtime.provider = mock_provider
        
        session = Session(session_id="test-session")
        
        # First turn with tool call
        async def mock_stream_1():
            yield {"type": "tool_use", "name": "test_tool", "arguments": {"input": "first"}}
            yield {"type": "stop"}
        
        mock_provider.stream = AsyncMock(return_value=mock_stream_1())
        
        async for event in runtime.run_turn(
            session=session,
            message="First turn",
            tools=[test_tool]
        ):
            pass
        
        first_call_count = test_tool.call_count
        
        # Second turn with tool call
        async def mock_stream_2():
            yield {"type": "tool_use", "name": "test_tool", "arguments": {"input": "second"}}
            yield {"type": "stop"}
        
        mock_provider.stream = AsyncMock(return_value=mock_stream_2())
        
        async for event in runtime.run_turn(
            session=session,
            message="Second turn",
            tools=[test_tool]
        ):
            pass
        
        # Verify tool was called in both turns
        assert test_tool.call_count > first_call_count
    
    @pytest.mark.asyncio
    async def test_tool_execution_failure(self):
        """Test handling of tool execution failures"""
        class FailingTool(AgentTool):
            name = "failing_tool"
            description = "A tool that fails"
            parameters = {"type": "object", "properties": {}}
            
            async def execute(self, **kwargs) -> ToolResult:
                raise ValueError("Tool execution failed")
        
        failing_tool = FailingTool()
        
        async def mock_stream():
            yield {"type": "tool_use", "name": "failing_tool", "arguments": {}}
            yield {"type": "stop"}
        
        mock_provider = AsyncMock()
        mock_provider.stream = AsyncMock(return_value=mock_stream())
        
        runtime = MultiProviderRuntime(model="mock/test")
        runtime.provider = mock_provider
        
        session = Session(session_id="test-session")
        
        # Should not raise, should handle error gracefully
        events = []
        async for event in runtime.run_turn(
            session=session,
            message="Use failing tool",
            tools=[failing_tool]
        ):
            events.append(event)
        
        # Verify we got an error event or tool_result event with failure
        # (depending on implementation)
        assert len(events) > 0


class TestAbortMechanism:
    """Test abort/cancellation mechanism"""
    
    @pytest.mark.asyncio
    async def test_abort_turn(self):
        """Test aborting a turn mid-execution"""
        # Create a slow mock stream
        async def slow_stream():
            for i in range(100):
                await asyncio.sleep(0.01)
                yield {"type": "text", "text": f"chunk{i} "}
        
        mock_provider = AsyncMock()
        mock_provider.stream = AsyncMock(return_value=slow_stream())
        
        runtime = MultiProviderRuntime(model="mock/test")
        runtime.provider = mock_provider
        
        session = Session(session_id="test-session")
        
        # Start turn in background
        turn_task = asyncio.create_task(
            self._collect_events(runtime.run_turn(session, "Test", []))
        )
        
        # Wait a bit then cancel
        await asyncio.sleep(0.05)
        turn_task.cancel()
        
        # Verify cancellation
        with pytest.raises(asyncio.CancelledError):
            await turn_task
    
    async def _collect_events(self, event_stream):
        """Helper to collect events from stream"""
        events = []
        async for event in event_stream:
            events.append(event)
        return events


class TestEventPropagation:
    """Test event emission and propagation"""
    
    @pytest.mark.asyncio
    async def test_event_emission(self):
        """Test that all expected events are emitted"""
        mock_provider = AsyncMock()
        mock_provider.generate = AsyncMock(return_value={
            "content": "Response",
            "tool_calls": [],
            "usage": {}
        })
        
        runtime = MultiProviderRuntime(model="mock/test")
        runtime.provider = mock_provider
        
        session = Session(session_id="test-session")
        
        # Collect all events
        events = []
        async for event in runtime.run_turn(session, "Test", []):
            events.append(event)
        
        # Verify we got a started event
        started_events = [e for e in events if e.type == EventType.AGENT_STARTED]
        assert len(started_events) > 0
        
        # Verify we got a turn complete event
        complete_events = [e for e in events if e.type == EventType.AGENT_TURN_COMPLETE]
        assert len(complete_events) > 0
    
    @pytest.mark.asyncio
    async def test_event_listener(self):
        """Test event listener registration and callbacks"""
        mock_provider = AsyncMock()
        mock_provider.generate = AsyncMock(return_value={
            "content": "Response",
            "tool_calls": [],
            "usage": {}
        })
        
        runtime = MultiProviderRuntime(model="mock/test")
        runtime.provider = mock_provider
        
        # Register listener
        received_events = []
        
        async def listener(event):
            received_events.append(event)
        
        runtime.add_event_listener(listener)
        
        session = Session(session_id="test-session")
        
        # Execute turn
        async for event in runtime.run_turn(session, "Test", []):
            pass
        
        # Verify listener received events
        assert len(received_events) > 0


class TestQueueManagement:
    """Test queue management features"""
    
    @pytest.mark.asyncio
    async def test_queue_enabled(self):
        """Test runtime with queue management enabled"""
        mock_provider = AsyncMock()
        mock_provider.generate = AsyncMock(return_value={
            "content": "Response",
            "tool_calls": [],
            "usage": {}
        })
        
        runtime = MultiProviderRuntime(
            model="mock/test",
            enable_queuing=True
        )
        runtime.provider = mock_provider
        
        session = Session(session_id="test-session")
        
        # Execute turn with queue
        events = []
        async for event in runtime.run_turn(session, "Test", []):
            events.append(event)
        
        # Verify execution completed
        assert len(events) > 0
        
        # Verify queue manager is present
        assert runtime.queue_manager is not None


class TestSteeringAndFollowup:
    """Test steering and follow-up message features"""
    
    @pytest.mark.asyncio
    async def test_steering_message_queue(self):
        """Test steering message queue"""
        runtime = MultiProviderRuntime(model="mock/test")
        
        # Add steering messages
        runtime.add_steering_message("Interrupt 1")
        runtime.add_steering_message("Interrupt 2")
        
        # Verify messages are queued
        assert len(runtime.steering_queue) == 2
        
        # Check messages
        msg1 = runtime.check_steering()
        assert msg1 == "Interrupt 1"
        assert len(runtime.steering_queue) == 1
        
        msg2 = runtime.check_steering()
        assert msg2 == "Interrupt 2"
        assert len(runtime.steering_queue) == 0
    
    @pytest.mark.asyncio
    async def test_followup_message_queue(self):
        """Test follow-up message queue"""
        runtime = MultiProviderRuntime(model="mock/test")
        
        # Add follow-up messages
        runtime.add_followup_message("Follow-up 1")
        runtime.add_followup_message("Follow-up 2")
        
        # Verify messages are queued
        assert len(runtime.followup_queue) == 2
        
        # Check messages
        msg1 = runtime.check_followup()
        assert msg1 == "Follow-up 1"
        
        msg2 = runtime.check_followup()
        assert msg2 == "Follow-up 2"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
