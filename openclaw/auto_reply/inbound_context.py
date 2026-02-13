"""
Inbound message context processing

This module implements message context building and normalization to match TypeScript's
inbound-context.ts functionality.
"""
from __future__ import annotations

import logging
import re
from typing import Any, Optional, TypedDict
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class MsgContext(BaseModel):
    """
    Message context for agent processing
    
    Represents a normalized inbound message with all relevant metadata.
    This matches TypeScript's MsgContext interface.
    """
    
    # Core message content
    Body: str
    """Main message body (normalized)"""
    
    BodyForAgent: Optional[str] = None
    """Body variant for agent (with sender metadata if needed)"""
    
    BodyForCommands: Optional[str] = None
    """Body variant for command processing"""
    
    CommandBody: Optional[str] = None
    """Command-specific body (without command prefix)"""
    
    RawBody: Optional[str] = None
    """Raw body before any processing"""
    
    Transcript: Optional[str] = None
    """Transcript of previous conversation"""
    
    ThreadStarterBody: Optional[str] = None
    """Body of thread starter message"""
    
    UntrustedContext: Optional[list[str]] = None
    """Untrusted context items (e.g., group history)"""
    
    # Session and routing
    SessionKey: str
    """Session key for conversation tracking"""
    
    From: Optional[str] = None
    """Sender identifier"""
    
    To: Optional[str] = None
    """Recipient identifier"""
    
    ChatType: Optional[str] = None
    """Chat type (dm, group, channel, etc.)"""
    
    ConversationLabel: Optional[str] = None
    """Human-readable conversation label"""
    
    # Media
    MediaPath: Optional[str] = None
    """Local path to downloaded media"""
    
    MediaUrls: Optional[list[str]] = None
    """URLs of media attachments"""
    
    # Reply context
    ReplyToId: Optional[str] = None
    """ID of message being replied to"""
    
    ReplyToBody: Optional[str] = None
    """Body of message being replied to"""
    
    # Flags
    WasMentioned: bool = False
    """Whether bot was mentioned in this message"""
    
    CommandAuthorized: bool = False
    """Whether sender is authorized for commands"""
    
    # Channel routing
    OriginatingChannel: Optional[str] = None
    """Original channel where message came from"""
    
    OriginatingTo: Optional[str] = None
    """Original recipient"""
    
    # Sender metadata
    SenderName: Optional[str] = None
    """Sender's display name"""
    
    SenderUsername: Optional[str] = None
    """Sender's username"""
    
    # Group context
    GroupId: Optional[str] = None
    """Group identifier"""
    
    GroupName: Optional[str] = None
    """Group display name"""
    
    TopicId: Optional[str | int] = None
    """Topic/thread ID"""
    
    TopicName: Optional[str] = None
    """Topic/thread name"""
    
    # Additional metadata
    MessageId: Optional[str] = None
    """Message identifier"""
    
    Timestamp: Optional[str] = None
    """Message timestamp"""
    
    Channel: Optional[str] = None
    """Current channel"""
    
    AccountId: Optional[str] = None
    """Account identifier"""

    model_config = {"extra": "allow"}


class FinalizedMsgContext(MsgContext):
    """
    Finalized message context with all normalizations applied
    
    This is the output of finalize_inbound_context()
    """
    pass


class FinalizeOptions(TypedDict, total=False):
    """Options for finalize_inbound_context"""
    force_body_for_agent: bool
    force_body_for_commands: bool
    force_chat_type: bool
    force_conversation_label: bool


# ============================================================================
# Text Normalization
# ============================================================================

def normalize_inbound_text_newlines(text: str) -> str:
    """
    Normalize newlines in inbound text
    
    Converts various newline styles to \n
    
    Args:
        text: Input text
        
    Returns:
        Normalized text
    """
    if not text:
        return ""
    
    # Replace \r\n with \n
    text = text.replace("\r\n", "\n")
    
    # Replace remaining \r with \n
    text = text.replace("\r", "\n")
    
    return text


def _normalize_text_field(value: Any) -> Optional[str]:
    """Normalize a text field value"""
    if not isinstance(value, str):
        return None
    return normalize_inbound_text_newlines(value)


# ============================================================================
# Chat Type Normalization
# ============================================================================

def normalize_chat_type(chat_type: Optional[str]) -> Optional[str]:
    """
    Normalize chat type to standard values
    
    Args:
        chat_type: Input chat type
        
    Returns:
        Normalized chat type (dm, group, channel, etc.)
    """
    if not chat_type:
        return None
    
    chat_type = chat_type.lower().strip()
    
    # Map variants to standard types
    type_map = {
        "private": "dm",
        "direct": "dm",
        "supergroup": "group",
        "public": "channel",
    }
    
    return type_map.get(chat_type, chat_type)


# ============================================================================
# Conversation Label
# ============================================================================

def resolve_conversation_label(ctx: MsgContext) -> Optional[str]:
    """
    Resolve conversation label from context
    
    Args:
        ctx: Message context
        
    Returns:
        Conversation label
    """
    # Use explicit label if present
    if ctx.ConversationLabel:
        return ctx.ConversationLabel
    
    # Build label from context
    if ctx.ChatType == "dm":
        # DM: use sender name/username
        if ctx.SenderName:
            return f"DM with {ctx.SenderName}"
        if ctx.SenderUsername:
            return f"DM with @{ctx.SenderUsername}"
        if ctx.From:
            return f"DM with {ctx.From}"
    
    elif ctx.ChatType == "group":
        # Group: use group name
        if ctx.GroupName:
            return ctx.GroupName
        if ctx.GroupId:
            return f"Group {ctx.GroupId}"
    
    elif ctx.ChatType == "channel":
        # Channel: use group name (same as group for Telegram)
        if ctx.GroupName:
            return ctx.GroupName
        if ctx.GroupId:
            return f"Channel {ctx.GroupId}"
    
    # Fallback
    return None


# ============================================================================
# Sender Metadata Formatting
# ============================================================================

def format_inbound_body_with_sender_meta(
    ctx: MsgContext,
    body: str,
) -> str:
    """
    Add sender metadata to message body for group/channel messages
    
    For group and channel messages, prepends sender information to help the agent
    understand who said what.
    
    Args:
        ctx: Message context
        body: Message body
        
    Returns:
        Body with sender metadata (if applicable)
    """
    # Only add metadata for group/channel messages
    if ctx.ChatType not in ["group", "channel"]:
        return body
    
    # Skip if body already has sender metadata (starts with name followed by colon)
    if body and re.match(r"^\[?[\w\s]+\]?\s*:\s", body):
        return body
    
    # Build sender identifier
    sender = None
    if ctx.SenderName:
        sender = ctx.SenderName
    elif ctx.SenderUsername:
        sender = f"@{ctx.SenderUsername}"
    elif ctx.From:
        sender = ctx.From
    
    if not sender:
        return body
    
    # Prepend sender metadata
    # Format: "SenderName: message"
    if body:
        return f"{sender}: {body}"
    
    return body


# ============================================================================
# Finalize Inbound Context
# ============================================================================

def finalize_inbound_context(
    ctx: MsgContext,
    opts: Optional[FinalizeOptions] = None,
) -> FinalizedMsgContext:
    """
    Finalize inbound message context
    
    Applies all normalizations and transformations to prepare context for agent processing.
    This matches TypeScript's finalizeInboundContext function.
    
    Args:
        ctx: Input message context
        opts: Finalization options
        
    Returns:
        Finalized message context
    """
    opts = opts or {}
    
    # Normalize main body
    ctx.Body = normalize_inbound_text_newlines(ctx.Body or "")
    
    # Normalize optional text fields
    ctx.RawBody = _normalize_text_field(ctx.RawBody)
    ctx.CommandBody = _normalize_text_field(ctx.CommandBody)
    ctx.Transcript = _normalize_text_field(ctx.Transcript)
    ctx.ThreadStarterBody = _normalize_text_field(ctx.ThreadStarterBody)
    
    # Normalize untrusted context
    if isinstance(ctx.UntrustedContext, list):
        normalized_untrusted = [
            normalize_inbound_text_newlines(entry)
            for entry in ctx.UntrustedContext
            if entry
        ]
        ctx.UntrustedContext = [entry for entry in normalized_untrusted if entry]
    
    # Normalize chat type
    chat_type = normalize_chat_type(ctx.ChatType)
    if chat_type and (opts.get("force_chat_type") or ctx.ChatType != chat_type):
        ctx.ChatType = chat_type
    
    # Set BodyForAgent
    if opts.get("force_body_for_agent"):
        body_for_agent_source = ctx.Body
    else:
        body_for_agent_source = ctx.BodyForAgent or ctx.Body
    
    ctx.BodyForAgent = normalize_inbound_text_newlines(body_for_agent_source)
    
    # Set BodyForCommands
    if opts.get("force_body_for_commands"):
        body_for_commands_source = ctx.CommandBody or ctx.RawBody or ctx.Body
    else:
        body_for_commands_source = (
            ctx.BodyForCommands
            or ctx.CommandBody
            or ctx.RawBody
            or ctx.Body
        )
    
    ctx.BodyForCommands = normalize_inbound_text_newlines(body_for_commands_source)
    
    # Resolve conversation label
    explicit_label = ctx.ConversationLabel
    if opts.get("force_conversation_label") or not explicit_label:
        resolved = resolve_conversation_label(ctx)
        if resolved:
            ctx.ConversationLabel = resolved
    
    # Add sender metadata to body for group/channel messages
    ctx.Body = format_inbound_body_with_sender_meta(ctx, ctx.Body)
    ctx.BodyForAgent = format_inbound_body_with_sender_meta(ctx, ctx.BodyForAgent)
    
    # Ensure CommandAuthorized is always set (default False)
    if ctx.CommandAuthorized is None:
        ctx.CommandAuthorized = False
    
    return FinalizedMsgContext(**ctx.model_dump())


# ============================================================================
# Helper Functions
# ============================================================================

def build_session_key_from_context(
    agent_id: str,
    channel: str,
    chat_type: str,
    peer_id: str,
    thread_id: Optional[str | int] = None,
) -> str:
    """
    Build session key from context components
    
    Args:
        agent_id: Agent identifier
        channel: Channel name (telegram, discord, etc.)
        chat_type: Chat type (dm, group, channel)
        peer_id: Peer identifier (user ID or group ID)
        thread_id: Thread ID (optional)
        
    Returns:
        Session key in format: agent:{id}:{channel}:{chat_type}:{peer_id}[:thread:{thread_id}]
    """
    from openclaw.routing.session_key import build_agent_peer_session_key
    
    # Determine peer kind
    if chat_type == "dm":
        peer_kind = "dm"
    elif chat_type == "group":
        peer_kind = "group"
    elif chat_type == "channel":
        peer_kind = "channel"
    else:
        peer_kind = "dm"  # Default fallback
    
    key = build_agent_peer_session_key(
        agent_id=agent_id,
        channel=channel,
        peer_kind=peer_kind,
        peer_id=peer_id,
    )
    
    # Add thread suffix if present
    if thread_id:
        key = f"{key}:thread:{thread_id}"
    
    return key
