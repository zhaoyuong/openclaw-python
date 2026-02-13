"""Mock LLM providers for testing"""
from typing import Any, AsyncIterator

from openclaw.agents.providers.base import LLMMessage, LLMProvider, LLMResponse


class SimpleMockProvider(LLMProvider):
    """Simple mock provider that returns predefined responses"""
    
    def __init__(self, responses: list[str] | None = None):
        """
        Initialize mock provider
        
        Args:
            responses: List of responses to return
        """
        super().__init__()
        self.responses = responses or ["Mock response"]
        self.call_count = 0
        self.last_messages: list[LLMMessage] = []
        self.last_model: str = ""
        self.last_tools: list[dict] | None = None
    
    async def stream(
        self,
        messages: list[LLMMessage],
        model: str,
        tools: list[dict] | None = None
    ) -> AsyncIterator[LLMResponse]:
        """Mock streaming"""
        self.call_count += 1
        self.last_messages = messages
        self.last_model = model
        self.last_tools = tools
        
        # Return response
        response_index = min(self.call_count - 1, len(self.responses) - 1)
        response_text = self.responses[response_index]
        
        # Split into words for streaming effect
        words = response_text.split()
        for word in words:
            yield LLMResponse(type="text_delta", content=word + " ")
        
        yield LLMResponse(type="done", content="")


class ToolCallingMockProvider(LLMProvider):
    """Mock provider that returns tool calls"""
    
    def __init__(self, tool_name: str, tool_params: dict[str, Any] | None = None):
        """
        Initialize tool calling mock provider
        
        Args:
            tool_name: Name of tool to call
            tool_params: Parameters for tool call
        """
        super().__init__()
        self.tool_name = tool_name
        self.tool_params = tool_params or {}
        self.call_count = 0
    
    async def stream(
        self,
        messages: list[LLMMessage],
        model: str,
        tools: list[dict] | None = None
    ) -> AsyncIterator[LLMResponse]:
        """Mock streaming with tool call"""
        self.call_count += 1
        
        if self.call_count == 1:
            # First call: return tool call
            yield LLMResponse(type="text_delta", content="I'll use the tool. ")
            yield LLMResponse(
                type="tool_call",
                tool_calls=[{
                    "id": f"call_{self.call_count}",
                    "name": self.tool_name,
                    "arguments": self.tool_params
                }]
            )
            yield LLMResponse(type="done", content="")
        else:
            # Subsequent calls: return text response
            yield LLMResponse(type="text_delta", content="Tool executed successfully.")
            yield LLMResponse(type="done", content="")


class ThinkingMockProvider(LLMProvider):
    """Mock provider that returns thinking content"""
    
    def __init__(self, thinking_text: str = "Let me think...", response_text: str = "Here's my response."):
        """
        Initialize thinking mock provider
        
        Args:
            thinking_text: Thinking content
            response_text: Final response
        """
        super().__init__()
        self.thinking_text = thinking_text
        self.response_text = response_text
    
    async def stream(
        self,
        messages: list[LLMMessage],
        model: str,
        tools: list[dict] | None = None
    ) -> AsyncIterator[LLMResponse]:
        """Mock streaming with thinking"""
        # Start thinking
        yield LLMResponse(type="thinking_start", content="")
        
        # Stream thinking
        for word in self.thinking_text.split():
            yield LLMResponse(type="thinking_delta", content=word + " ")
        
        # End thinking
        yield LLMResponse(type="thinking_end", content=self.thinking_text)
        
        # Stream response
        for word in self.response_text.split():
            yield LLMResponse(type="text_delta", content=word + " ")
        
        yield LLMResponse(type="done", content="")


class ErrorMockProvider(LLMProvider):
    """Mock provider that raises errors"""
    
    def __init__(self, error_message: str = "Mock error"):
        """
        Initialize error mock provider
        
        Args:
            error_message: Error message to raise
        """
        super().__init__()
        self.error_message = error_message
    
    async def stream(
        self,
        messages: list[LLMMessage],
        model: str,
        tools: list[dict] | None = None
    ) -> AsyncIterator[LLMResponse]:
        """Mock streaming that raises error"""
        raise Exception(self.error_message)


class ConversationalMockProvider(LLMProvider):
    """Mock provider with conversational responses"""
    
    def __init__(self):
        """Initialize conversational mock provider"""
        super().__init__()
        self.conversation_history: list[dict] = []
    
    async def stream(
        self,
        messages: list[LLMMessage],
        model: str,
        tools: list[dict] | None = None
    ) -> AsyncIterator[LLMResponse]:
        """Mock streaming with context-aware responses"""
        # Record conversation
        self.conversation_history.append({
            "messages": messages,
            "model": model
        })
        
        # Get last user message
        user_messages = [m for m in messages if m.role == "user"]
        if user_messages:
            last_message = user_messages[-1].content.lower()
            
            # Context-aware responses
            if "hello" in last_message or "hi" in last_message:
                response = "Hello! How can I help you today?"
            elif "bye" in last_message or "goodbye" in last_message:
                response = "Goodbye! Have a great day!"
            elif "?" in last_message:
                response = "That's a great question. Let me think about that."
            else:
                response = "I understand. Is there anything else you'd like to know?"
        else:
            response = "Hello!"
        
        # Stream response
        for word in response.split():
            yield LLMResponse(type="text_delta", content=word + " ")
        
        yield LLMResponse(type="done", content="")
