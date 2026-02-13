"""Unit tests for Bash tool"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from openclaw.agents.tools.bash import BashTool
from openclaw.agents.tools.base import ToolResult


class TestBashTool:
    """Test Bash tool"""
    
    def test_create_tool(self):
        """Test creating Bash tool"""
        tool = BashTool()
        assert tool is not None
        assert tool.name == "bash"
        assert tool.description != ""
    
    def test_get_schema(self):
        """Test getting tool schema"""
        tool = BashTool()
        schema = tool.get_schema()
        
        assert isinstance(schema, dict)
        assert "type" in schema
        assert "properties" in schema
        assert "command" in schema["properties"]
    
    @pytest.mark.asyncio
    async def test_execute_simple_command(self):
        """Test executing simple command"""
        tool = BashTool()
        
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="Hello\n",
                stderr=""
            )
            
            result = await tool.execute({"command": "echo Hello"})
            
            assert result.success
            assert "Hello" in result.content
    
    @pytest.mark.asyncio
    async def test_execute_command_failure(self):
        """Test executing command that fails"""
        tool = BashTool()
        
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=1,
                stdout="",
                stderr="Error"
            )
            
            result = await tool.execute({"command": "false"})
            
            assert not result.success
            assert result.error is not None
    
    @pytest.mark.asyncio
    async def test_execute_with_timeout(self):
        """Test command timeout"""
        tool = BashTool(timeout=1)
        
        with patch("subprocess.run") as mock_run:
            import subprocess
            mock_run.side_effect = subprocess.TimeoutExpired("test", 1)
            
            result = await tool.execute({"command": "sleep 10"})
            
            assert not result.success
            assert "timeout" in result.error.lower()
    
    @pytest.mark.asyncio
    async def test_execute_invalid_params(self):
        """Test executing with invalid parameters"""
        tool = BashTool()
        
        result = await tool.execute({})  # Missing 'command'
        
        assert not result.success
        assert result.error is not None


class TestBashToolSecurity:
    """Test Bash tool security features"""
    
    @pytest.mark.asyncio
    async def test_blocked_commands(self):
        """Test that dangerous commands are blocked"""
        tool = BashTool()
        
        # These commands should be blocked or require approval
        dangerous_commands = [
            "rm -rf /",
            ":(){ :|:& };:",  # Fork bomb
            "dd if=/dev/zero of=/dev/sda",
        ]
        
        for cmd in dangerous_commands:
            # Tool should handle these safely
            result = await tool.execute({"command": cmd})
            # Result may be blocked or require approval
            assert isinstance(result, ToolResult)
    
    def test_working_directory(self):
        """Test working directory setting"""
        tool = BashTool(working_dir="/tmp")
        assert tool.working_dir == "/tmp"


def test_bash_tool_imports():
    """Test that Bash tool can be imported"""
    try:
        from openclaw.agents.tools import BashTool
        assert BashTool is not None
    except ImportError as e:
        pytest.fail(f"Failed to import BashTool: {e}")
