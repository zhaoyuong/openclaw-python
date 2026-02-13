"""Error recovery tests

Tests system's ability to handle and recover from errors:
- LLM API failures
- Tool execution failures  
- Network interruptions
- Resource exhaustion
- Invalid inputs
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, Mock, patch

from openclaw.gateway.server import GatewayServer, GatewayConnection
from openclaw.agents.runtime import MultiProviderRuntime
from openclaw.agents.session import Session
from openclaw.agents.tools.base import AgentTool, ToolResult
from openclaw.config.schema import ClawdbotConfig


class TestLLMAPIFailures:
    """Test LLM API failure handling"""
    
    @pytest.mark.asyncio
    async def test_api_timeout_recovery(self):
        """Test recovery from API timeout"""
        config = ClawdbotConfig()
        
        mock_runtime = AsyncMock(spec=MultiProviderRuntime)
        
        attempt_count = 0
        
        async def mock_turn(*args, **kwargs):
            nonlocal attempt_count
            attempt_count += 1
            
            if attempt_count == 1:
                # First attempt times out
                await asyncio.sleep(0.1)
                raise asyncio.TimeoutError("API timeout")
            else:
                # Retry succeeds
                yield Mock(type="text", data={"text": "Success after timeout"})
        
        mock_runtime.run_turn = lambda *args, **kwargs: mock_turn(*args, **kwargs)
        
        server = GatewayServer(
            config=config,
            agent_runtime=mock_runtime,
            session_manager=Mock()
        )
        
        from tests.test_gateway_agent_integration import MockWebSocket
        import json
        
        # First request (timeout)
        ws1 = MockWebSocket()
        connection1 = GatewayConnection(ws1, config, gateway=server)
        connection1.authenticated = True
        
        request1 = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "agent",
            "params": {"message": "Test", "sessionId": "test-session"}
        }
        
        try:
            await connection1.handle_message(json.dumps(request1))
        except Exception:
            pass  # Timeout expected
        
        # Retry request (success)
        ws2 = MockWebSocket()
        connection2 = GatewayConnection(ws2, config, gateway=server)
        connection2.authenticated = True
        
        request2 = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "agent",
            "params": {"message": "Test retry", "sessionId": "test-session"}
        }
        
        await connection2.handle_message(json.dumps(request2))
        
        # Verify retry succeeded
        assert attempt_count == 2
    
    @pytest.mark.asyncio
    async def test_api_rate_limit_recovery(self):
        """Test recovery from rate limiting"""
        runtime = MultiProviderRuntime(model="mock/test")
        runtime.provider = AsyncMock()
        
        # Simulate rate limit then success
        runtime.provider.generate = AsyncMock(
            side_effect=[
                Exception("Rate limit exceeded"),
                {
                    "content": "Success after rate limit",
                    "tool_calls": [],
                    "usage": {}
                }
            ]
        )
        
        session = Session(session_id="test-session")
        
        # First turn fails with rate limit
        try:
            async for event in runtime.run_turn(session, "Test", []):
                pass
        except Exception:
            pass  # Expected to fail
        
        # Wait before retry (simulate backoff)
        await asyncio.sleep(0.01)
        
        # Retry should succeed
        events = []
        async for event in runtime.run_turn(session, "Test retry", []):
            events.append(event)
        
        assert len(events) > 0
    
    @pytest.mark.asyncio
    async def test_api_invalid_response_recovery(self):
        """Test recovery from invalid API response"""
        config = ClawdbotConfig()
        
        mock_runtime = AsyncMock(spec=MultiProviderRuntime)
        
        call_count = 0
        
        async def mock_turn(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            
            if call_count == 1:
                # Invalid response
                raise ValueError("Invalid JSON in API response")
            else:
                # Valid response
                yield Mock(type="text", data={"text": "Valid response"})
        
        mock_runtime.run_turn = lambda *args, **kwargs: mock_turn(*args, **kwargs)
        
        server = GatewayServer(
            config=config,
            agent_runtime=mock_runtime,
            session_manager=Mock()
        )
        
        from tests.test_gateway_agent_integration import MockWebSocket
        import json
        
        # Handle invalid response
        ws1 = MockWebSocket()
        connection1 = GatewayConnection(ws1, config, gateway=server)
        connection1.authenticated = True
        
        try:
            await connection1.handle_message(json.dumps({
                "jsonrpc": "2.0",
                "id": 1,
                "method": "agent",
                "params": {"message": "Test", "sessionId": "test"}
            }))
        except Exception:
            pass
        
        # Retry with valid response
        ws2 = MockWebSocket()
        connection2 = GatewayConnection(ws2, config, gateway=server)
        connection2.authenticated = True
        
        await connection2.handle_message(json.dumps({
            "jsonrpc": "2.0",
            "id": 2,
            "method": "agent",
            "params": {"message": "Test retry", "sessionId": "test"}
        }))
        
        assert call_count == 2


class TestToolExecutionFailures:
    """Test tool execution failure handling"""
    
    @pytest.mark.asyncio
    async def test_tool_exception_handling(self):
        """Test handling of tool exceptions"""
        
        class FailingTool(AgentTool):
            name = "failing_tool"
            description = "A tool that fails"
            parameters = {"type": "object", "properties": {}}
            
            async def execute(self, **kwargs) -> ToolResult:
                raise RuntimeError("Tool execution failed")
        
        failing_tool = FailingTool()
        
        runtime = MultiProviderRuntime(model="mock/test")
        runtime.provider = AsyncMock()
        
        async def mock_stream(*args, **kwargs):
            yield {"type": "tool_use", "name": "failing_tool", "arguments": {}}
            yield {"type": "stop"}
        
        runtime.provider.stream = AsyncMock(return_value=mock_stream())
        
        session = Session(session_id="test-session")
        
        # Should handle tool failure gracefully
        events = []
        try:
            async for event in runtime.run_turn(session, "Test", [failing_tool]):
                events.append(event)
        except Exception as e:
            # Should not propagate exception
            pytest.fail(f"Tool exception was not handled: {e}")
        
        # Verify execution continued despite tool failure
        assert len(events) > 0
    
    @pytest.mark.asyncio
    async def test_tool_timeout_handling(self):
        """Test handling of tool timeouts"""
        
        class SlowTool(AgentTool):
            name = "slow_tool"
            description = "A slow tool"
            parameters = {"type": "object", "properties": {}}
            
            async def execute(self, **kwargs) -> ToolResult:
                await asyncio.sleep(10)  # Very slow
                return ToolResult(success=True, output="Done")
        
        slow_tool = SlowTool()
        
        runtime = MultiProviderRuntime(model="mock/test")
        runtime.provider = AsyncMock()
        
        async def mock_stream(*args, **kwargs):
            yield {"type": "tool_use", "name": "slow_tool", "arguments": {}}
            yield {"type": "stop"}
        
        runtime.provider.stream = AsyncMock(return_value=mock_stream())
        
        session = Session(session_id="test-session")
        
        # Execute with timeout
        task = asyncio.create_task(
            self._collect_events(runtime.run_turn(session, "Test", [slow_tool]))
        )
        
        # Cancel after short time
        await asyncio.sleep(0.1)
        task.cancel()
        
        # Should handle cancellation
        with pytest.raises(asyncio.CancelledError):
            await task
    
    async def _collect_events(self, event_stream):
        """Helper to collect events"""
        events = []
        async for event in event_stream:
            events.append(event)
        return events


class TestNetworkInterruptions:
    """Test network interruption handling"""
    
    @pytest.mark.asyncio
    async def test_connection_loss_recovery(self):
        """Test recovery from connection loss"""
        config = ClawdbotConfig()
        
        mock_runtime = AsyncMock(spec=MultiProviderRuntime)
        
        async def mock_turn(*args, **kwargs):
            yield Mock(type="text", data={"text": "Response"})
        
        mock_runtime.run_turn = lambda *args, **kwargs: mock_turn(*args, **kwargs)
        
        server = GatewayServer(
            config=config,
            agent_runtime=mock_runtime,
            session_manager=Mock()
        )
        
        from tests.test_gateway_agent_integration import MockWebSocket
        
        # Create connection
        ws = MockWebSocket()
        connection = GatewayConnection(ws, config, gateway=server)
        connection.authenticated = True
        
        # Simulate connection loss
        ws.closed = True
        
        # Try to send message (should handle gracefully)
        try:
            await connection.send_event("test", {"data": "test"})
        except Exception:
            pass  # Expected to fail
        
        # Create new connection (reconnect)
        ws2 = MockWebSocket()
        connection2 = GatewayConnection(ws2, config, gateway=server)
        connection2.authenticated = True
        
        # Should work after reconnect
        import json
        await connection2.handle_message(json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "agent",
            "params": {"message": "Test", "sessionId": "test"}
        }))
        
        assert len(ws2.sent_messages) > 0


class TestResourceExhaustion:
    """Test resource exhaustion scenarios"""
    
    @pytest.mark.asyncio
    async def test_queue_full_handling(self):
        """Test handling of full queue"""
        config = ClawdbotConfig()
        
        mock_runtime = AsyncMock(spec=MultiProviderRuntime)
        mock_runtime.queue_manager = Mock()
        
        # Simulate full queue
        mock_runtime.queue_manager.get_global_lane = Mock()
        mock_runtime.queue_manager.get_global_lane.return_value.get_stats = Mock(
            return_value={
                "queued": 100,
                "active": 100,
                "max_concurrent": 10
            }
        )
        
        async def mock_turn(*args, **kwargs):
            yield Mock(type="error", data={"message": "Queue is full"})
        
        mock_runtime.run_turn = lambda *args, **kwargs: mock_turn(*args, **kwargs)
        
        server = GatewayServer(
            config=config,
            agent_runtime=mock_runtime,
            session_manager=Mock()
        )
        
        from tests.test_gateway_agent_integration import MockWebSocket
        import json
        
        ws = MockWebSocket()
        connection = GatewayConnection(ws, config, gateway=server)
        connection.authenticated = True
        
        # Should handle queue full gracefully
        await connection.handle_message(json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "agent",
            "params": {"message": "Test", "sessionId": "test"}
        }))
        
        # Should receive error response
        assert len(ws.sent_messages) > 0


class TestInvalidInputs:
    """Test invalid input handling"""
    
    @pytest.mark.asyncio
    async def test_invalid_method(self):
        """Test handling of invalid method"""
        config = ClawdbotConfig()
        
        server = GatewayServer(
            config=config,
            agent_runtime=Mock(),
            session_manager=Mock()
        )
        
        from tests.test_gateway_agent_integration import MockWebSocket
        import json
        
        ws = MockWebSocket()
        connection = GatewayConnection(ws, config, gateway=server)
        connection.authenticated = True
        
        # Send invalid method
        await connection.handle_message(json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "invalid.method.name",
            "params": {}
        }))
        
        # Should receive error response
        assert len(ws.sent_messages) > 0
        
        response = json.loads(ws.sent_messages[0])
        assert "error" in response
    
    @pytest.mark.asyncio
    async def test_missing_required_params(self):
        """Test handling of missing required parameters"""
        config = ClawdbotConfig()
        
        server = GatewayServer(
            config=config,
            agent_runtime=Mock(),
            session_manager=Mock()
        )
        
        from tests.test_gateway_agent_integration import MockWebSocket
        import json
        
        ws = MockWebSocket()
        connection = GatewayConnection(ws, config, gateway=server)
        connection.authenticated = True
        
        # Send request without required message param
        await connection.handle_message(json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "agent",
            "params": {}  # Missing 'message'
        }))
        
        # Should receive error response
        assert len(ws.sent_messages) > 0
    
    @pytest.mark.asyncio
    async def test_malformed_json(self):
        """Test handling of malformed JSON"""
        config = ClawdbotConfig()
        
        server = GatewayServer(
            config=config,
            agent_runtime=Mock(),
            session_manager=Mock()
        )
        
        from tests.test_gateway_agent_integration import MockWebSocket
        
        ws = MockWebSocket()
        connection = GatewayConnection(ws, config, gateway=server)
        connection.authenticated = True
        
        # Send malformed JSON
        try:
            await connection.handle_message("{invalid json}")
        except Exception:
            pass  # Expected to fail
        
        # Connection should still be usable
        import json
        await connection.handle_message(json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "ping",
            "params": {}
        }))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
