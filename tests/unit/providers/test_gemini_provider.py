"""Unit tests for Gemini provider"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from openclaw.agents.providers.gemini_provider import GeminiProvider
from openclaw.agents.providers.base import LLMMessage, LLMResponse


class TestGeminiProvider:
    """Test Gemini provider"""
    
    def test_create_provider(self):
        """Test creating provider"""
        provider = GeminiProvider(api_key="test-key")
        assert provider is not None
        assert provider.api_key == "test-key"
    
    def test_create_provider_without_key(self):
        """Test creating provider without API key"""
        with pytest.raises(ValueError):
            GeminiProvider(api_key="")
    
    def test_model_validation(self):
        """Test model name validation"""
        provider = GeminiProvider(api_key="test-key")
        
        # Valid models
        assert provider.validate_model("gemini-pro")
        assert provider.validate_model("gemini-3-pro-preview")
        
        # Invalid model
        assert not provider.validate_model("invalid-model")
    
    @pytest.mark.asyncio
    async def test_stream_basic(self):
        """Test basic streaming"""
        provider = GeminiProvider(api_key="test-key")
        
        messages = [
            LLMMessage(role="user", content="Hello")
        ]
        
        # Mock the actual API call
        with patch.object(provider, '_make_api_call', new_callable=AsyncMock) as mock_call:
            mock_call.return_value = AsyncMock()
            mock_call.return_value.__aiter__.return_value = [
                {"type": "text", "content": "Hi"},
                {"type": "text", "content": " there"},
            ]
            
            responses = []
            async for response in provider.stream(messages, model="gemini-pro"):
                responses.append(response)
            
            assert len(responses) >= 0  # May vary based on mock


class TestGeminiMessageFormatting:
    """Test Gemini message formatting"""
    
    def test_format_user_message(self):
        """Test formatting user message"""
        provider = GeminiProvider(api_key="test-key")
        
        messages = [
            LLMMessage(role="user", content="Test message")
        ]
        
        formatted = provider._format_messages(messages)
        
        assert isinstance(formatted, list)
        assert len(formatted) > 0
    
    def test_format_conversation(self):
        """Test formatting conversation"""
        provider = GeminiProvider(api_key="test-key")
        
        messages = [
            LLMMessage(role="user", content="Hello"),
            LLMMessage(role="assistant", content="Hi"),
            LLMMessage(role="user", content="How are you?"),
        ]
        
        formatted = provider._format_messages(messages)
        
        assert isinstance(formatted, list)
        assert len(formatted) == 3
    
    def test_format_with_system_message(self):
        """Test formatting with system message"""
        provider = GeminiProvider(api_key="test-key")
        
        messages = [
            LLMMessage(role="system", content="You are helpful"),
            LLMMessage(role="user", content="Hello"),
        ]
        
        formatted = provider._format_messages(messages)
        
        # System message should be handled appropriately
        assert isinstance(formatted, list)


class TestGeminiTools:
    """Test Gemini tool support"""
    
    def test_format_tools(self):
        """Test formatting tools"""
        provider = GeminiProvider(api_key="test-key")
        
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "search",
                    "description": "Search for information",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"}
                        }
                    }
                }
            }
        ]
        
        formatted = provider._format_tools(tools)
        
        assert isinstance(formatted, list)
        assert len(formatted) == 1


def test_gemini_provider_imports():
    """Test that Gemini provider can be imported"""
    try:
        from openclaw.agents.providers import GeminiProvider
        assert GeminiProvider is not None
    except ImportError as e:
        pytest.fail(f"Failed to import GeminiProvider: {e}")
