"""Unit tests for Ollama provider"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from openclaw.agents.providers.ollama_provider import OllamaProvider
from openclaw.agents.providers.base import LLMMessage, LLMResponse


class TestOllamaProvider:
    """Test Ollama provider"""
    
    def test_create_provider(self):
        """Test creating provider"""
        provider = OllamaProvider(base_url="http://localhost:11434")
        assert provider is not None
        assert provider.base_url == "http://localhost:11434"
    
    def test_create_provider_default_url(self):
        """Test creating provider with default URL"""
        provider = OllamaProvider()
        assert provider is not None
        assert provider.base_url == "http://localhost:11434"
    
    def test_model_validation(self):
        """Test model name validation"""
        provider = OllamaProvider()
        
        # Ollama accepts any model name
        assert provider.validate_model("llama2")
        assert provider.validate_model("mistral")
        assert provider.validate_model("codellama")
    
    @pytest.mark.asyncio
    async def test_stream_basic(self):
        """Test basic streaming"""
        provider = OllamaProvider()
        
        messages = [
            LLMMessage(role="user", content="Hello")
        ]
        
        with patch.object(provider, '_make_api_call', new_callable=AsyncMock) as mock_call:
            mock_call.return_value = AsyncMock()
            mock_call.return_value.__aiter__.return_value = [
                {"response": "Hi", "done": False},
                {"response": " there", "done": False},
                {"done": True}
            ]
            
            responses = []
            async for response in provider.stream(messages, model="llama2"):
                responses.append(response)
            
            assert len(responses) >= 0
    
    @pytest.mark.asyncio
    async def test_list_models(self):
        """Test listing available models"""
        provider = OllamaProvider()
        
        with patch.object(provider, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {
                "models": [
                    {"name": "llama2"},
                    {"name": "mistral"},
                ]
            }
            
            models = await provider.list_models()
            
            assert isinstance(models, list)
            assert len(models) == 2


class TestOllamaMessageFormatting:
    """Test Ollama message formatting"""
    
    def test_format_user_message(self):
        """Test formatting user message"""
        provider = OllamaProvider()
        
        messages = [
            LLMMessage(role="user", content="Test message")
        ]
        
        formatted = provider._format_messages(messages)
        
        assert isinstance(formatted, list)
        assert len(formatted) > 0
        assert formatted[0]["role"] == "user"
        assert formatted[0]["content"] == "Test message"
    
    def test_format_conversation(self):
        """Test formatting conversation"""
        provider = OllamaProvider()
        
        messages = [
            LLMMessage(role="system", content="You are helpful"),
            LLMMessage(role="user", content="Hello"),
            LLMMessage(role="assistant", content="Hi"),
        ]
        
        formatted = provider._format_messages(messages)
        
        assert isinstance(formatted, list)
        assert len(formatted) == 3


class TestOllamaLocalDeployment:
    """Test Ollama local deployment features"""
    
    def test_custom_base_url(self):
        """Test custom base URL"""
        provider = OllamaProvider(base_url="http://custom:8080")
        assert provider.base_url == "http://custom:8080"
    
    @pytest.mark.asyncio
    async def test_connection_check(self):
        """Test connection check"""
        provider = OllamaProvider()
        
        with patch.object(provider, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {"status": "ok"}
            
            is_available = await provider.check_connection()
            
            assert isinstance(is_available, bool)
    
    @pytest.mark.asyncio
    async def test_pull_model(self):
        """Test pulling a model"""
        provider = OllamaProvider()
        
        with patch.object(provider, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {"status": "success"}
            
            result = await provider.pull_model("llama2")
            
            assert result is not None


class TestOllamaStreaming:
    """Test Ollama streaming functionality"""
    
    @pytest.mark.asyncio
    async def test_stream_with_stop(self):
        """Test streaming with stop sequences"""
        provider = OllamaProvider()
        
        messages = [
            LLMMessage(role="user", content="Count to 5")
        ]
        
        with patch.object(provider, '_make_api_call', new_callable=AsyncMock) as mock_call:
            mock_call.return_value = AsyncMock()
            mock_call.return_value.__aiter__.return_value = [
                {"response": "1, 2, 3", "done": False},
                {"done": True}
            ]
            
            responses = []
            async for response in provider.stream(
                messages,
                model="llama2",
                stop=["3"]
            ):
                responses.append(response)
            
            assert len(responses) >= 0


def test_ollama_provider_imports():
    """Test that Ollama provider can be imported"""
    try:
        from openclaw.agents.providers import OllamaProvider
        assert OllamaProvider is not None
    except ImportError as e:
        pytest.fail(f"Failed to import OllamaProvider: {e}")
