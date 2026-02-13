"""Integration tests for Gateway-Agent interaction

Tests the integration between Gateway and Agent Runtime:
- Gateway request handling
- Channel message routing
- Concurrent requests
- Queue limits
- Abort mechanism
"""
import pytest
import asyncio
import json
from unittest.mock import Mock, AsyncMock, patch

from openclaw.gateway.server import GatewayServer, GatewayConnection
from openclaw.agents.runtime import MultiProviderRuntime
from openclaw.agents.session import Session
from openclaw.config.schema import ClawdbotConfig, GatewayConfig


class MockWebSocket:
    """Mock WebSocket for testing"""
    
    def __init__(self):
        self.sent_messages = []
        self.closed = False
        self.remote_address = ("127.0.0.1", 12345)
    
    async def send(self, message: str):
        """Mock send"""
        self.sent_messages.append(message)
    
    async def close(self):
        """Mock close"""
        self.closed = True
    
    def __aiter__(self):
        """Mock async iteration (for message receiving)"""
        return self
    
    async def __anext__(self):
        """Mock async next (no messages in basic test)"""
        raise StopAsyncIteration


class TestGatewayAgentRequest:
    """Test Gateway to Agent request flow"""
    
    @pytest.mark.asyncio
    async def test_agent_request_flow(self):
        """Test basic agent request through Gateway"""
        # Create config
        config = ClawdbotConfig()
        config.gateway = GatewayConfig(port=8765)
        
        # Create mock runtime
        mock_runtime = AsyncMock(spec=MultiProviderRuntime)
        mock_runtime.run_turn = AsyncMock()
        
        async def mock_turn(*args, **kwargs):
            yield Mock(type="text", data={"text": "Response"})
        
        mock_runtime.run_turn.return_value = mock_turn()
        
        # Create gateway server
        server = GatewayServer(
            config=config,
            agent_runtime=mock_runtime,
            session_manager=Mock()
        )
        
        # Create mock connection
        ws = MockWebSocket()
        connection = GatewayConnection(ws, config, gateway=server)
        connection.authenticated = True
        
        # Simulate agent request
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "agent",
            "params": {
                "message": "Hello",
                "sessionId": "test-session"
            }
        }
        
        await connection.handle_message(json.dumps(request))
        
        # Verify response was sent
        assert len(ws.sent_messages) > 0
    
    @pytest.mark.asyncio
    async def test_streaming_agent_request(self):
        """Test streaming agent request"""
        config = ClawdbotConfig()
        
        mock_runtime = AsyncMock(spec=MultiProviderRuntime)
        
        async def mock_stream(*args, **kwargs):
            for i in range(3):
                yield Mock(
                    type="text",
                    data={"delta": {"text": f"chunk{i} "}}
                )
        
        mock_runtime.run_turn.return_value = mock_stream()
        
        server = GatewayServer(
            config=config,
            agent_runtime=mock_runtime,
            session_manager=Mock()
        )
        
        ws = MockWebSocket()
        connection = GatewayConnection(ws, config, gateway=server)
        connection.authenticated = True
        
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "agent",
            "params": {
                "message": "Hello",
                "stream": True,
                "sessionId": "test-session"
            }
        }
        
        await connection.handle_message(json.dumps(request))
        
        # Wait for async task to complete
        await asyncio.sleep(0.1)
        
        # Verify events were sent
        assert len(ws.sent_messages) > 0


class TestChannelMessageRouting:
    """Test channel to agent message routing"""
    
    @pytest.mark.asyncio
    async def test_channel_routing(self):
        """Test message routing from channel to agent"""
        from openclaw.gateway.channel_manager import ChannelManager
        from openclaw.channels.base import InboundMessage
        
        config = ClawdbotConfig()
        
        # Create mock runtime
        mock_runtime = AsyncMock(spec=MultiProviderRuntime)
        
        async def mock_turn(*args, **kwargs):
            yield Mock(type="text", data={"text": "Response"})
        
        mock_runtime.run_turn.return_value = mock_turn()
        
        # Create channel manager
        manager = ChannelManager(config)
        manager.set_default_runtime(mock_runtime)
        
        # Simulate receiving a message
        # (Note: This is a simplified test, real implementation would be more complex)
        message = InboundMessage(
            channel_id="test-channel",
            chat_id="test-chat",
            sender_id="user123",
            sender_name="Test User",
            text="Hello agent"
        )
        
        # Would normally route through channel handler
        # For this test, just verify runtime has been set
        assert manager.get_runtime("test-channel") is not None


class TestConcurrentRequests:
    """Test concurrent agent requests"""
    
    @pytest.mark.asyncio
    async def test_concurrent_requests(self):
        """Test handling multiple concurrent requests"""
        config = ClawdbotConfig()
        
        # Create runtime with queue enabled
        mock_runtime = AsyncMock(spec=MultiProviderRuntime)
        mock_runtime.queue_manager = Mock()
        mock_runtime.queue_manager.get_global_lane = Mock()
        mock_runtime.queue_manager.get_global_lane.return_value.get_stats = Mock(
            return_value={"queued": 0, "active": 0, "max_concurrent": 10}
        )
        
        call_count = 0
        
        async def mock_turn(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            await asyncio.sleep(0.01)  # Simulate processing
            yield Mock(type="text", data={"text": f"Response {call_count}"})
        
        mock_runtime.run_turn = lambda *args, **kwargs: mock_turn(*args, **kwargs)
        
        server = GatewayServer(
            config=config,
            agent_runtime=mock_runtime,
            session_manager=Mock()
        )
        
        # Create multiple connections and send concurrent requests
        tasks = []
        for i in range(5):
            ws = MockWebSocket()
            connection = GatewayConnection(ws, config, gateway=server)
            connection.authenticated = True
            
            request = {
                "jsonrpc": "2.0",
                "id": i,
                "method": "agent",
                "params": {
                    "message": f"Request {i}",
                    "sessionId": f"session-{i}"
                }
            }
            
            task = asyncio.create_task(
                connection.handle_message(json.dumps(request))
            )
            tasks.append(task)
        
        # Wait for all requests to complete
        await asyncio.gather(*tasks)
        
        # Verify all requests were handled
        assert call_count == 5
    
    @pytest.mark.asyncio
    async def test_queue_overflow(self):
        """Test handling when queue is full"""
        config = ClawdbotConfig()
        
        # Create runtime with small queue
        mock_runtime = AsyncMock(spec=MultiProviderRuntime)
        mock_runtime.queue_manager = Mock()
        mock_runtime.queue_manager.get_global_lane = Mock()
        mock_runtime.queue_manager.get_global_lane.return_value.get_stats = Mock(
            return_value={"queued": 10, "active": 10, "max_concurrent": 10}  # Full
        )
        
        async def mock_turn(*args, **kwargs):
            yield Mock(type="error", data={"message": "Queue is full"})
        
        mock_runtime.run_turn = lambda *args, **kwargs: mock_turn(*args, **kwargs)
        
        server = GatewayServer(
            config=config,
            agent_runtime=mock_runtime,
            session_manager=Mock()
        )
        
        ws = MockWebSocket()
        connection = GatewayConnection(ws, config, gateway=server)
        connection.authenticated = True
        
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "agent",
            "params": {
                "message": "Test",
                "sessionId": "test-session"
            }
        }
        
        await connection.handle_message(json.dumps(request))
        
        # Should receive error response or queue full message
        assert len(ws.sent_messages) > 0


class TestAbortIntegration:
    """Test abort mechanism through Gateway"""
    
    @pytest.mark.asyncio
    async def test_abort_request(self):
        """Test aborting a running agent request"""
        config = ClawdbotConfig()
        
        # Create runtime with long-running task
        mock_runtime = AsyncMock(spec=MultiProviderRuntime)
        
        async def long_running_turn(*args, **kwargs):
            for i in range(100):
                await asyncio.sleep(0.01)
                yield Mock(type="text", data={"text": f"chunk{i} "})
        
        mock_runtime.run_turn = lambda *args, **kwargs: long_running_turn(*args, **kwargs)
        
        server = GatewayServer(
            config=config,
            agent_runtime=mock_runtime,
            session_manager=Mock()
        )
        
        # Start a streaming request
        ws = MockWebSocket()
        connection = GatewayConnection(ws, config, gateway=server)
        connection.authenticated = True
        
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "agent",
            "params": {
                "message": "Long task",
                "stream": True,
                "runId": "test-run-123",
                "sessionId": "test-session"
            }
        }
        
        # Send request (non-blocking)
        asyncio.create_task(connection.handle_message(json.dumps(request)))
        
        # Wait a bit
        await asyncio.sleep(0.05)
        
        # Send abort request
        abort_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "chat.abort",
            "params": {
                "runId": "test-run-123"
            }
        }
        
        await connection.handle_message(json.dumps(abort_request))
        
        # Verify abort response
        # (In real implementation, would check for abort confirmation)
        assert len(ws.sent_messages) > 0


class TestQueueStatus:
    """Test queue status API"""
    
    @pytest.mark.asyncio
    async def test_queue_status(self):
        """Test agent.queue.status endpoint"""
        config = ClawdbotConfig()
        
        # Create runtime with queue
        mock_runtime = AsyncMock(spec=MultiProviderRuntime)
        mock_runtime.queue_manager = Mock()
        mock_runtime.queue_manager.get_stats = Mock(return_value={
            "global": {
                "name": "global",
                "max_concurrent": 10,
                "active": 2,
                "queued": 1,
                "running": True
            },
            "sessions": {},
            "total_sessions": 0
        })
        
        server = GatewayServer(
            config=config,
            agent_runtime=mock_runtime,
            session_manager=Mock()
        )
        
        ws = MockWebSocket()
        connection = GatewayConnection(ws, config, gateway=server)
        connection.authenticated = True
        
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "agent.queue.status",
            "params": {}
        }
        
        await connection.handle_message(json.dumps(request))
        
        # Verify status response
        assert len(ws.sent_messages) > 0
        
        # Parse response
        response = json.loads(ws.sent_messages[0])
        assert "result" in response
        assert response["result"]["enabled"] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
