"""Stress and performance tests

Tests system behavior under load:
- High concurrency
- Large messages
- Memory usage
- Response times
"""
import pytest
import asyncio
import time
import psutil
import os
from unittest.mock import AsyncMock, Mock

from openclaw.gateway.server import GatewayServer, GatewayConnection
from openclaw.agents.runtime import MultiProviderRuntime
from openclaw.agents.session import Session
from openclaw.config.schema import ClawdbotConfig


class TestHighConcurrency:
    """Test high concurrency scenarios"""
    
    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_100_concurrent_requests(self):
        """Test handling 100 concurrent requests"""
        config = ClawdbotConfig()
        
        # Create mock runtime
        mock_runtime = AsyncMock(spec=MultiProviderRuntime)
        
        request_count = 0
        
        async def mock_turn(*args, **kwargs):
            nonlocal request_count
            request_count += 1
            await asyncio.sleep(0.001)  # Minimal processing time
            yield Mock(type="text", data={"text": f"Response {request_count}"})
        
        mock_runtime.run_turn = lambda *args, **kwargs: mock_turn(*args, **kwargs)
        
        server = GatewayServer(
            config=config,
            agent_runtime=mock_runtime,
            session_manager=Mock()
        )
        
        # Send 100 concurrent requests
        from tests.test_gateway_agent_integration import MockWebSocket
        import json
        
        start_time = time.time()
        tasks = []
        
        for i in range(100):
            ws = MockWebSocket()
            connection = GatewayConnection(ws, config, gateway=server)
            connection.authenticated = True
            
            request = {
                "jsonrpc": "2.0",
                "id": i,
                "method": "agent",
                "params": {
                    "message": f"Request {i}",
                    "sessionId": f"session-{i % 10}"  # 10 different sessions
                }
            }
            
            task = asyncio.create_task(
                connection.handle_message(json.dumps(request))
            )
            tasks.append(task)
        
        # Wait for all to complete
        await asyncio.gather(*tasks)
        
        elapsed = time.time() - start_time
        
        # Verify all completed
        assert request_count == 100
        
        # Performance check (should handle 100 requests in reasonable time)
        print(f"Handled 100 concurrent requests in {elapsed:.2f}s")
        assert elapsed < 10.0  # Should complete in under 10 seconds
    
    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_sustained_load(self):
        """Test sustained load over time"""
        config = ClawdbotConfig()
        
        mock_runtime = AsyncMock(spec=MultiProviderRuntime)
        
        async def mock_turn(*args, **kwargs):
            await asyncio.sleep(0.01)
            yield Mock(type="text", data={"text": "Response"})
        
        mock_runtime.run_turn = lambda *args, **kwargs: mock_turn(*args, **kwargs)
        
        server = GatewayServer(
            config=config,
            agent_runtime=mock_runtime,
            session_manager=Mock()
        )
        
        from tests.test_gateway_agent_integration import MockWebSocket
        import json
        
        # Send requests continuously for 5 seconds
        start_time = time.time()
        request_count = 0
        
        while time.time() - start_time < 5.0:
            ws = MockWebSocket()
            connection = GatewayConnection(ws, config, gateway=server)
            connection.authenticated = True
            
            request = {
                "jsonrpc": "2.0",
                "id": request_count,
                "method": "agent",
                "params": {
                    "message": "Test",
                    "sessionId": "test-session"
                }
            }
            
            await connection.handle_message(json.dumps(request))
            request_count += 1
            
            # Small delay between requests
            await asyncio.sleep(0.05)
        
        elapsed = time.time() - start_time
        throughput = request_count / elapsed
        
        print(f"Handled {request_count} requests in {elapsed:.2f}s ({throughput:.1f} req/s)")
        assert request_count > 50  # Should handle at least 50 requests in 5 seconds


class TestLargeMessages:
    """Test handling of large messages"""
    
    @pytest.mark.asyncio
    async def test_large_input_message(self):
        """Test handling large input messages (100K characters)"""
        config = ClawdbotConfig()
        
        mock_runtime = AsyncMock(spec=MultiProviderRuntime)
        
        received_message = None
        
        async def mock_turn(session, message, *args, **kwargs):
            nonlocal received_message
            received_message = message
            yield Mock(type="text", data={"text": "Processed large message"})
        
        mock_runtime.run_turn = mock_turn
        
        server = GatewayServer(
            config=config,
            agent_runtime=mock_runtime,
            session_manager=Mock()
        )
        
        from tests.test_gateway_agent_integration import MockWebSocket
        import json
        
        # Create 100K character message
        large_message = "A" * 100_000
        
        ws = MockWebSocket()
        connection = GatewayConnection(ws, config, gateway=server)
        connection.authenticated = True
        
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "agent",
            "params": {
                "message": large_message,
                "sessionId": "test-session"
            }
        }
        
        await connection.handle_message(json.dumps(request))
        
        # Verify message was received
        assert received_message == large_message
    
    @pytest.mark.asyncio
    async def test_large_response_stream(self):
        """Test streaming large responses"""
        config = ClawdbotConfig()
        
        mock_runtime = AsyncMock(spec=MultiProviderRuntime)
        
        # Generate large streaming response (10K chunks)
        async def mock_turn(*args, **kwargs):
            for i in range(10_000):
                yield Mock(type="text", data={"delta": {"text": "A"}})
        
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
        
        start_time = time.time()
        
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "agent",
            "params": {
                "message": "Generate large response",
                "stream": True,
                "sessionId": "test-session"
            }
        }
        
        await connection.handle_message(json.dumps(request))
        
        # Wait for stream to complete
        await asyncio.sleep(0.1)
        
        elapsed = time.time() - start_time
        
        print(f"Streamed 10K chunks in {elapsed:.2f}s")


class TestMemoryUsage:
    """Test memory usage under load"""
    
    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_memory_stability(self):
        """Test memory doesn't grow unbounded"""
        config = ClawdbotConfig()
        
        mock_runtime = AsyncMock(spec=MultiProviderRuntime)
        
        async def mock_turn(*args, **kwargs):
            # Create some temporary data
            _ = "x" * 1000
            yield Mock(type="text", data={"text": "Response"})
        
        mock_runtime.run_turn = lambda *args, **kwargs: mock_turn(*args, **kwargs)
        
        server = GatewayServer(
            config=config,
            agent_runtime=mock_runtime,
            session_manager=Mock()
        )
        
        from tests.test_gateway_agent_integration import MockWebSocket
        import json
        
        # Get initial memory
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Execute many requests
        for i in range(100):
            ws = MockWebSocket()
            connection = GatewayConnection(ws, config, gateway=server)
            connection.authenticated = True
            
            request = {
                "jsonrpc": "2.0",
                "id": i,
                "method": "agent",
                "params": {
                    "message": "Test",
                    "sessionId": f"session-{i}"
                }
            }
            
            await connection.handle_message(json.dumps(request))
        
        # Get final memory
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_growth = final_memory - initial_memory
        
        print(f"Memory: {initial_memory:.1f}MB -> {final_memory:.1f}MB (growth: {memory_growth:.1f}MB)")
        
        # Memory growth should be reasonable (< 100MB for 100 requests)
        assert memory_growth < 100


class TestResponseTimes:
    """Test response time performance"""
    
    @pytest.mark.asyncio
    async def test_average_response_time(self):
        """Test average response time for requests"""
        config = ClawdbotConfig()
        
        mock_runtime = AsyncMock(spec=MultiProviderRuntime)
        
        async def mock_turn(*args, **kwargs):
            await asyncio.sleep(0.01)  # Simulate 10ms processing
            yield Mock(type="text", data={"text": "Response"})
        
        mock_runtime.run_turn = lambda *args, **kwargs: mock_turn(*args, **kwargs)
        
        server = GatewayServer(
            config=config,
            agent_runtime=mock_runtime,
            session_manager=Mock()
        )
        
        from tests.test_gateway_agent_integration import MockWebSocket
        import json
        
        response_times = []
        
        for i in range(20):
            ws = MockWebSocket()
            connection = GatewayConnection(ws, config, gateway=server)
            connection.authenticated = True
            
            request = {
                "jsonrpc": "2.0",
                "id": i,
                "method": "agent",
                "params": {
                    "message": "Test",
                    "sessionId": "test-session"
                }
            }
            
            start = time.time()
            await connection.handle_message(json.dumps(request))
            elapsed = time.time() - start
            
            response_times.append(elapsed)
        
        avg_response_time = sum(response_times) / len(response_times)
        max_response_time = max(response_times)
        
        print(f"Avg response time: {avg_response_time*1000:.1f}ms")
        print(f"Max response time: {max_response_time*1000:.1f}ms")
        
        # Average should be reasonable
        assert avg_response_time < 0.1  # < 100ms average
        assert max_response_time < 0.5  # < 500ms max


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "not slow"])
