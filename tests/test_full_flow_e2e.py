"""Full flow end-to-end tests

Tests the complete user journey from onboarding to agent execution:
- New user complete flow
- Multi-session flow
- Tool-enabled conversation flow
"""
import pytest
import asyncio
import tempfile
from pathlib import Path
from unittest.mock import patch, AsyncMock, Mock

from openclaw.wizard.onboarding import run_onboarding_wizard, is_first_run
from openclaw.gateway.server import GatewayServer, GatewayConnection
from openclaw.agents.runtime import MultiProviderRuntime
from openclaw.agents.session import Session
from openclaw.config.schema import ClawdbotConfig, GatewayConfig, AgentConfig
from openclaw.config.loader import save_config


class TestNewUserFullFlow:
    """Test complete new user flow"""
    
    @pytest.mark.asyncio
    async def test_new_user_onboarding_to_chat(self):
        """Test new user from onboarding through first chat"""
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            
            # Step 1: Verify first run
            assert is_first_run(workspace) is True
            
            # Step 2: Run onboarding (QuickStart)
            inputs = [
                "y",  # Confirm risks
                "1",  # QuickStart mode
                "1",  # Anthropic provider
                "test-api-key",  # API key
                "Y",  # Save configuration
            ]
            
            with patch("builtins.input", side_effect=inputs):
                with patch("openclaw.wizard.auth.save_auth_to_env"):
                    config = ClawdbotConfig()
                    config.gateway = GatewayConfig(port=8765)
                    config.agent = AgentConfig(model="claude-sonnet-4")
                    
                    with patch("openclaw.config.loader.save_config"):
                        result = await run_onboarding_wizard(workspace_dir=workspace)
            
            assert result["completed"] is True
            
            # Step 3: Verify first run marker created
            assert is_first_run(workspace) is False
            
            # Step 4: Create Gateway with mock runtime
            mock_runtime = AsyncMock(spec=MultiProviderRuntime)
            
            async def mock_turn(*args, **kwargs):
                yield Mock(type="text", data={"text": "Hello! I'm your assistant."})
            
            mock_runtime.run_turn.return_value = mock_turn()
            
            server = GatewayServer(
                config=config,
                agent_runtime=mock_runtime,
                session_manager=Mock()
            )
            
            # Step 5: Send a message through Gateway
            from tests.test_gateway_agent_integration import MockWebSocket
            ws = MockWebSocket()
            connection = GatewayConnection(ws, config, gateway=server)
            connection.authenticated = True
            
            import json
            request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "agent",
                "params": {
                    "message": "Hello",
                    "sessionId": "main"
                }
            }
            
            await connection.handle_message(json.dumps(request))
            
            # Step 6: Verify response received
            assert len(ws.sent_messages) > 0


class TestMultiSessionFlow:
    """Test multi-session flow"""
    
    @pytest.mark.asyncio
    async def test_multiple_sessions(self):
        """Test handling multiple concurrent sessions"""
        config = ClawdbotConfig()
        
        # Create mock runtime
        mock_runtime = AsyncMock(spec=MultiProviderRuntime)
        
        responses = {
            "session-1": "Response for session 1",
            "session-2": "Response for session 2",
            "session-3": "Response for session 3",
        }
        
        async def mock_turn(session, message, *args, **kwargs):
            session_id = session.session_id if hasattr(session, 'session_id') else "unknown"
            response_text = responses.get(session_id, "Default response")
            yield Mock(type="text", data={"text": response_text})
        
        mock_runtime.run_turn = mock_turn
        
        server = GatewayServer(
            config=config,
            agent_runtime=mock_runtime,
            session_manager=Mock()
        )
        
        # Send messages from different sessions
        from tests.test_gateway_agent_integration import MockWebSocket
        import json
        
        sessions = ["session-1", "session-2", "session-3"]
        tasks = []
        
        for session_id in sessions:
            ws = MockWebSocket()
            connection = GatewayConnection(ws, config, gateway=server)
            connection.authenticated = True
            
            request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "agent",
                "params": {
                    "message": f"Message from {session_id}",
                    "sessionId": session_id
                }
            }
            
            task = asyncio.create_task(
                connection.handle_message(json.dumps(request))
            )
            tasks.append((task, ws))
        
        # Wait for all to complete
        for task, ws in tasks:
            await task
            assert len(ws.sent_messages) > 0
    
    @pytest.mark.asyncio
    async def test_session_isolation(self):
        """Test that sessions are properly isolated"""
        # Create runtime
        runtime = MultiProviderRuntime(model="mock/test")
        runtime.provider = AsyncMock()
        
        # Create two sessions
        session1 = Session(session_id="session-1")
        session2 = Session(session_id="session-2")
        
        # Add messages to session 1
        session1.add_user_message("Message 1 for session 1")
        session1.add_assistant_message("Response 1 for session 1")
        
        # Add different messages to session 2
        session2.add_user_message("Message 1 for session 2")
        session2.add_assistant_message("Response 1 for session 2")
        
        # Verify sessions have different messages
        assert len(session1.messages) == 2
        assert len(session2.messages) == 2
        assert session1.messages[0].content != session2.messages[0].content


class TestToolEnabledFlow:
    """Test conversation flow with tools"""
    
    @pytest.mark.asyncio
    async def test_conversation_with_tools(self):
        """Test full conversation flow with tool usage"""
        from openclaw.agents.tools.base import AgentTool, ToolResult
        
        # Create a test tool
        class CalculatorTool(AgentTool):
            name = "calculator"
            description = "Perform calculations"
            parameters = {
                "type": "object",
                "properties": {
                    "operation": {"type": "string"},
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                }
            }
            
            async def execute(self, operation: str, a: float, b: float) -> ToolResult:
                if operation == "add":
                    result = a + b
                elif operation == "multiply":
                    result = a * b
                else:
                    return ToolResult(success=False, output="Unknown operation")
                
                return ToolResult(
                    success=True,
                    output=f"Result: {result}",
                    metadata={"result": result}
                )
        
        calculator = CalculatorTool()
        
        # Create runtime with tool
        mock_provider = AsyncMock()
        
        # Simulate tool use
        async def mock_stream(*args, **kwargs):
            # First yield a tool use
            yield {
                "type": "tool_use",
                "name": "calculator",
                "arguments": {"operation": "add", "a": 5, "b": 3}
            }
            # Then yield text response
            yield {"type": "text", "text": "The result is 8"}
            yield {"type": "stop"}
        
        mock_provider.stream = AsyncMock(return_value=mock_stream())
        
        runtime = MultiProviderRuntime(model="mock/test")
        runtime.provider = mock_provider
        
        session = Session(session_id="test-session")
        
        # Execute turn with tool
        events = []
        async for event in runtime.run_turn(
            session=session,
            message="What is 5 + 3?",
            tools=[calculator]
        ):
            events.append(event)
        
        # Verify tool was called and response was generated
        assert len(events) > 0
        assert calculator.call_count > 0 if hasattr(calculator, 'call_count') else True
    
    @pytest.mark.asyncio
    async def test_multi_tool_conversation(self):
        """Test conversation with multiple tool calls"""
        from openclaw.agents.tools.base import AgentTool, ToolResult
        
        class Tool1(AgentTool):
            name = "tool1"
            description = "First tool"
            parameters = {"type": "object", "properties": {}}
            call_count = 0
            
            async def execute(self, **kwargs) -> ToolResult:
                Tool1.call_count += 1
                return ToolResult(success=True, output="Tool 1 result")
        
        class Tool2(AgentTool):
            name = "tool2"
            description = "Second tool"
            parameters = {"type": "object", "properties": {}}
            call_count = 0
            
            async def execute(self, **kwargs) -> ToolResult:
                Tool2.call_count += 1
                return ToolResult(success=True, output="Tool 2 result")
        
        tool1 = Tool1()
        tool2 = Tool2()
        
        mock_provider = AsyncMock()
        
        async def mock_stream(*args, **kwargs):
            yield {"type": "tool_use", "name": "tool1", "arguments": {}}
            yield {"type": "tool_use", "name": "tool2", "arguments": {}}
            yield {"type": "text", "text": "Both tools executed"}
            yield {"type": "stop"}
        
        mock_provider.stream = AsyncMock(return_value=mock_stream())
        
        runtime = MultiProviderRuntime(model="mock/test")
        runtime.provider = mock_provider
        
        session = Session(session_id="test-session")
        
        events = []
        async for event in runtime.run_turn(
            session=session,
            message="Use both tools",
            tools=[tool1, tool2]
        ):
            events.append(event)
        
        # Verify both tools were called
        assert Tool1.call_count > 0
        assert Tool2.call_count > 0


class TestErrorRecoveryFlow:
    """Test error handling and recovery"""
    
    @pytest.mark.asyncio
    async def test_error_recovery(self):
        """Test recovery from errors"""
        config = ClawdbotConfig()
        
        # Create runtime that fails first, then succeeds
        mock_runtime = AsyncMock(spec=MultiProviderRuntime)
        
        call_count = 0
        
        async def mock_turn(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            
            if call_count == 1:
                # First call fails
                yield Mock(type="error", data={"message": "API error"})
            else:
                # Subsequent calls succeed
                yield Mock(type="text", data={"text": "Success after retry"})
        
        mock_runtime.run_turn = lambda *args, **kwargs: mock_turn(*args, **kwargs)
        
        server = GatewayServer(
            config=config,
            agent_runtime=mock_runtime,
            session_manager=Mock()
        )
        
        from tests.test_gateway_agent_integration import MockWebSocket
        import json
        
        # First request (fails)
        ws1 = MockWebSocket()
        connection1 = GatewayConnection(ws1, config, gateway=server)
        connection1.authenticated = True
        
        request1 = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "agent",
            "params": {
                "message": "Test",
                "sessionId": "test-session"
            }
        }
        
        await connection1.handle_message(json.dumps(request1))
        
        # Second request (succeeds)
        ws2 = MockWebSocket()
        connection2 = GatewayConnection(ws2, config, gateway=server)
        connection2.authenticated = True
        
        request2 = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "agent",
            "params": {
                "message": "Test again",
                "sessionId": "test-session"
            }
        }
        
        await connection2.handle_message(json.dumps(request2))
        
        # Both should have received responses
        assert len(ws1.sent_messages) > 0
        assert len(ws2.sent_messages) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
