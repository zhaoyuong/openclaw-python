"""
Tests for context processing alignment

Tests:
- Message context finalization
- Text normalization  
- Chat type normalization
- Sender metadata formatting
- Conversation label resolution
"""
import pytest

from openclaw.auto_reply.inbound_context import (
    MsgContext,
    finalize_inbound_context,
    normalize_inbound_text_newlines,
    normalize_chat_type,
    resolve_conversation_label,
    format_inbound_body_with_sender_meta,
)


class TestTextNormalization:
    """Test text normalization"""
    
    def test_newline_normalization(self):
        """Test newline styles are normalized"""
        # Windows style
        text = "Line 1\r\nLine 2\r\nLine 3"
        normalized = normalize_inbound_text_newlines(text)
        assert normalized == "Line 1\nLine 2\nLine 3"
        
        # Mac style
        text = "Line 1\rLine 2\rLine 3"
        normalized = normalize_inbound_text_newlines(text)
        assert normalized == "Line 1\nLine 2\nLine 3"
        
        # Mixed
        text = "Line 1\r\nLine 2\rLine 3\nLine 4"
        normalized = normalize_inbound_text_newlines(text)
        assert normalized == "Line 1\nLine 2\nLine 3\nLine 4"


class TestChatTypeNormalization:
    """Test chat type normalization"""
    
    def test_standard_types(self):
        """Test standard chat types"""
        assert normalize_chat_type("dm") == "dm"
        assert normalize_chat_type("group") == "group"
        assert normalize_chat_type("channel") == "channel"
    
    def test_variant_mapping(self):
        """Test variant types are mapped"""
        assert normalize_chat_type("private") == "dm"
        assert normalize_chat_type("direct") == "dm"
        assert normalize_chat_type("supergroup") == "group"
        assert normalize_chat_type("public") == "channel"
    
    def test_case_insensitive(self):
        """Test case insensitive"""
        assert normalize_chat_type("DM") == "dm"
        assert normalize_chat_type("GROUP") == "group"
        assert normalize_chat_type("Private") == "dm"


class TestConversationLabel:
    """Test conversation label resolution"""
    
    def test_dm_label(self):
        """Test DM conversation label"""
        ctx = MsgContext(
            Body="Hello",
            SessionKey="test",
            ChatType="dm",
            SenderName="John Doe",
        )
        label = resolve_conversation_label(ctx)
        assert label == "DM with John Doe"
    
    def test_dm_with_username(self):
        """Test DM with username only"""
        ctx = MsgContext(
            Body="Hello",
            SessionKey="test",
            ChatType="dm",
            SenderUsername="johndoe",
        )
        label = resolve_conversation_label(ctx)
        assert label == "DM with @johndoe"
    
    def test_group_label(self):
        """Test group conversation label"""
        ctx = MsgContext(
            Body="Hello",
            SessionKey="test",
            ChatType="group",
            GroupName="My Awesome Group",
        )
        label = resolve_conversation_label(ctx)
        assert label == "My Awesome Group"
    
    def test_explicit_label(self):
        """Test explicit label is preserved"""
        ctx = MsgContext(
            Body="Hello",
            SessionKey="test",
            ChatType="group",
            ConversationLabel="Custom Label",
            GroupName="Should not use this",
        )
        label = resolve_conversation_label(ctx)
        assert label == "Custom Label"


class TestSenderMetadata:
    """Test sender metadata formatting"""
    
    def test_group_message_formatting(self):
        """Test sender metadata is added to group messages"""
        ctx = MsgContext(
            Body="Hello",
            SessionKey="test",
            ChatType="group",
            SenderName="Alice",
        )
        formatted = format_inbound_body_with_sender_meta(ctx, "Hello everyone!")
        assert formatted == "Alice: Hello everyone!"
    
    def test_dm_no_formatting(self):
        """Test DMs don't get sender metadata"""
        ctx = MsgContext(
            Body="Hello",
            SessionKey="test",
            ChatType="dm",
            SenderName="Alice",
        )
        formatted = format_inbound_body_with_sender_meta(ctx, "Hello!")
        assert formatted == "Hello!"
    
    def test_already_formatted(self):
        """Test already formatted messages are not re-formatted"""
        ctx = MsgContext(
            Body="Hello",
            SessionKey="test",
            ChatType="group",
            SenderName="Alice",
        )
        formatted = format_inbound_body_with_sender_meta(ctx, "Alice: Hello!")
        # Should not add another prefix
        assert formatted == "Alice: Hello!"


class TestContextFinalization:
    """Test complete context finalization"""
    
    def test_basic_finalization(self):
        """Test basic context finalization"""
        ctx = MsgContext(
            Body="Hello\r\nWorld",
            SessionKey="test-key",
            ChatType="private",
            SenderName="John",
        )
        
        finalized = finalize_inbound_context(ctx)
        
        # Body normalized
        assert finalized.Body == "Hello\nWorld"
        
        # Chat type normalized
        assert finalized.ChatType == "dm"
        
        # BodyForAgent set
        assert finalized.BodyForAgent == "Hello\nWorld"
        
        # BodyForCommands set
        assert finalized.BodyForCommands == "Hello\nWorld"
        
        # CommandAuthorized defaulted
        assert finalized.CommandAuthorized is False
        
        # Conversation label resolved
        assert finalized.ConversationLabel == "DM with John"
    
    def test_group_message_finalization(self):
        """Test group message finalization with sender meta"""
        ctx = MsgContext(
            Body="Hey team!",
            SessionKey="group-key",
            ChatType="group",
            SenderName="Alice",
            GroupName="Dev Team",
            WasMentioned=True,
        )
        
        finalized = finalize_inbound_context(ctx)
        
        # Sender metadata added
        assert finalized.Body == "Alice: Hey team!"
        assert finalized.BodyForAgent == "Alice: Hey team!"
        
        # Conversation label
        assert finalized.ConversationLabel == "Dev Team"
        
        # Flags preserved
        assert finalized.WasMentioned is True
    
    def test_untrusted_context_normalization(self):
        """Test untrusted context is normalized"""
        ctx = MsgContext(
            Body="Hello",
            SessionKey="test",
            UntrustedContext=["Line 1\r\n", "Line 2", "", "Line 3\r"],
        )
        
        finalized = finalize_inbound_context(ctx)
        
        # Empty strings removed, newlines normalized
        assert len(finalized.UntrustedContext) == 3
        assert finalized.UntrustedContext[0] == "Line 1\n"
        assert finalized.UntrustedContext[1] == "Line 2"
        assert finalized.UntrustedContext[2] == "Line 3\n"
    
    def test_body_variants(self):
        """Test different body variants are handled"""
        ctx = MsgContext(
            Body="Normal body",
            RawBody="Raw body\r\n",
            CommandBody="Command body",
            SessionKey="test",
        )
        
        finalized = finalize_inbound_context(ctx)
        
        # All normalized
        assert finalized.Body == "Normal body"
        assert finalized.RawBody == "Raw body\n"
        assert finalized.CommandBody == "Command body"
        
        # BodyForAgent defaults to Body
        assert finalized.BodyForAgent == "Normal body"
        
        # BodyForCommands uses CommandBody
        assert finalized.BodyForCommands == "Command body"


@pytest.mark.parametrize("chat_type,sender_name,expected_label", [
    ("dm", "Alice", "DM with Alice"),
    ("group", None, None),  # No group name
    ("channel", None, None),  # No channel name
])
def test_label_resolution_cases(chat_type, sender_name, expected_label):
    """Test various label resolution cases"""
    ctx = MsgContext(
        Body="Test",
        SessionKey="test",
        ChatType=chat_type,
        SenderName=sender_name,
    )
    label = resolve_conversation_label(ctx)
    assert label == expected_label


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
