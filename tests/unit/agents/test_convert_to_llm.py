"""Unit tests for message conversion"""
import pytest

from openclaw.agents.agent_loop import AgentMessage, default_convert_to_llm
from openclaw.agents.providers.base import LLMMessage


class TestMessageConversion:
    """Test message conversion from AgentMessage to LLMMessage"""
    
    def test_convert_user_message(self):
        """Test converting user message"""
        messages = [AgentMessage(role="user", content="Hello")]
        llm_messages = default_convert_to_llm(messages)
        
        assert len(llm_messages) == 1
        assert llm_messages[0].role == "user"
        assert llm_messages[0].content == "Hello"
    
    def test_convert_assistant_message(self):
        """Test converting assistant message"""
        messages = [AgentMessage(role="assistant", content="Hi there")]
        llm_messages = default_convert_to_llm(messages)
        
        assert len(llm_messages) == 1
        assert llm_messages[0].role == "assistant"
        assert llm_messages[0].content == "Hi there"
    
    def test_convert_system_message(self):
        """Test converting system message"""
        messages = [AgentMessage(role="system", content="You are helpful")]
        llm_messages = default_convert_to_llm(messages)
        
        assert len(llm_messages) == 1
        assert llm_messages[0].role == "system"
        assert llm_messages[0].content == "You are helpful"
    
    def test_filter_custom_messages(self):
        """Test filtering custom messages"""
        messages = [
            AgentMessage(role="user", content="Hello"),
            AgentMessage(role="custom", content="Internal note", custom=True),
            AgentMessage(role="assistant", content="Hi"),
        ]
        llm_messages = default_convert_to_llm(messages)
        
        # Custom message should be filtered out
        assert len(llm_messages) == 2
        assert llm_messages[0].content == "Hello"
        assert llm_messages[1].content == "Hi"
    
    def test_preserve_images(self):
        """Test preserving image attachments"""
        messages = [
            AgentMessage(
                role="user",
                content="What's in this image?",
                images=["data:image/png;base64,abc123"]
            )
        ]
        llm_messages = default_convert_to_llm(messages)
        
        assert len(llm_messages) == 1
        assert llm_messages[0].images is not None
        assert len(llm_messages[0].images) == 1
        assert llm_messages[0].images[0] == "data:image/png;base64,abc123"
    
    def test_preserve_tool_calls(self):
        """Test preserving tool calls"""
        tool_calls = [
            {"id": "call_1", "name": "search", "params": {"query": "test"}}
        ]
        messages = [
            AgentMessage(
                role="assistant",
                content="Let me search for that",
                tool_calls=tool_calls
            )
        ]
        llm_messages = default_convert_to_llm(messages)
        
        assert len(llm_messages) == 1
        assert llm_messages[0].tool_calls is not None
        assert len(llm_messages[0].tool_calls) == 1
        assert llm_messages[0].tool_calls[0]["name"] == "search"
    
    def test_preserve_tool_call_id(self):
        """Test preserving tool call ID in results"""
        messages = [
            AgentMessage(
                role="toolResult",
                content="Search results here",
                tool_call_id="call_1"
            )
        ]
        llm_messages = default_convert_to_llm(messages)
        
        assert len(llm_messages) == 1
        assert llm_messages[0].tool_call_id == "call_1"
    
    def test_convert_conversation(self):
        """Test converting full conversation"""
        messages = [
            AgentMessage(role="system", content="You are helpful"),
            AgentMessage(role="user", content="Hello"),
            AgentMessage(role="assistant", content="Hi, how can I help?"),
            AgentMessage(role="user", content="What's 2+2?"),
            AgentMessage(role="assistant", content="4"),
        ]
        llm_messages = default_convert_to_llm(messages)
        
        assert len(llm_messages) == 5
        assert llm_messages[0].role == "system"
        assert llm_messages[1].role == "user"
        assert llm_messages[2].role == "assistant"
        assert llm_messages[3].role == "user"
        assert llm_messages[4].role == "assistant"
    
    def test_empty_messages(self):
        """Test converting empty message list"""
        messages = []
        llm_messages = default_convert_to_llm(messages)
        
        assert len(llm_messages) == 0
    
    def test_metadata_not_converted(self):
        """Test that metadata is not converted to LLM messages"""
        messages = [
            AgentMessage(
                role="user",
                content="Test",
                metadata={"internal": "data"}
            )
        ]
        llm_messages = default_convert_to_llm(messages)
        
        # LLMMessage doesn't have metadata field
        assert len(llm_messages) == 1
        assert not hasattr(llm_messages[0], "metadata")
    
    def test_multiple_custom_messages_filtered(self):
        """Test filtering multiple custom messages"""
        messages = [
            AgentMessage(role="user", content="Hello"),
            AgentMessage(role="custom", content="Note 1", custom=True),
            AgentMessage(role="assistant", content="Hi"),
            AgentMessage(role="custom", content="Note 2", custom=True),
            AgentMessage(role="user", content="Thanks"),
        ]
        llm_messages = default_convert_to_llm(messages)
        
        assert len(llm_messages) == 3
        assert llm_messages[0].content == "Hello"
        assert llm_messages[1].content == "Hi"
        assert llm_messages[2].content == "Thanks"
    
    def test_message_with_multiple_images(self):
        """Test message with multiple images"""
        messages = [
            AgentMessage(
                role="user",
                content="Compare these images",
                images=[
                    "data:image/png;base64,abc",
                    "data:image/png;base64,def"
                ]
            )
        ]
        llm_messages = default_convert_to_llm(messages)
        
        assert len(llm_messages) == 1
        assert len(llm_messages[0].images) == 2


class TestCustomConversion:
    """Test custom conversion functions"""
    
    def test_custom_convert_function(self):
        """Test using custom conversion function"""
        def custom_converter(messages):
            # Custom logic: add prefix to all user messages
            llm_msgs = []
            for msg in messages:
                if msg.custom:
                    continue
                llm_msg = LLMMessage(role=msg.role, content=msg.content)
                if msg.role == "user":
                    llm_msg.content = f"[USER] {msg.content}"
                llm_msgs.append(llm_msg)
            return llm_msgs
        
        messages = [
            AgentMessage(role="user", content="Hello"),
            AgentMessage(role="assistant", content="Hi"),
        ]
        
        llm_messages = custom_converter(messages)
        
        assert len(llm_messages) == 2
        assert llm_messages[0].content == "[USER] Hello"
        assert llm_messages[1].content == "Hi"
