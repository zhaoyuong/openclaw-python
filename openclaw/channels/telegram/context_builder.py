"""
Telegram message context builder

Builds complete message context from Telegram updates, including:
- Sender information extraction
- Mention detection and parsing
- Reply context extraction
- Media handling
- Session key building
- Group history context
- Mention gating
- Command authorization
"""
from __future__ import annotations

import logging
import re
from typing import Any, Optional

from telegram import Message, Update, User, Chat

from openclaw.auto_reply.inbound_context import (
    MsgContext,
    finalize_inbound_context,
    build_session_key_from_context,
)

logger = logging.getLogger(__name__)


# ============================================================================
# Sender Information
# ============================================================================

def extract_sender_info(message: Message) -> dict[str, Optional[str]]:
    """
    Extract sender information from Telegram message
    
    Args:
        message: Telegram message
        
    Returns:
        Dict with sender_id, sender_name, sender_username
    """
    sender = message.from_user
    if not sender:
        return {
            "sender_id": None,
            "sender_name": None,
            "sender_username": None,
        }
    
    return {
        "sender_id": str(sender.id),
        "sender_name": sender.full_name,
        "sender_username": sender.username,
    }


# ============================================================================
# Chat Type Resolution
# ============================================================================

def resolve_telegram_chat_type(chat: Chat) -> str:
    """
    Resolve Telegram chat type to standard format
    
    Args:
        chat: Telegram chat object
        
    Returns:
        Standard chat type (dm, group, channel)
    """
    chat_type = chat.type.lower()
    
    # Map Telegram types to standard types
    type_map = {
        "private": "dm",
        "group": "group",
        "supergroup": "group",
        "channel": "channel",
    }
    
    return type_map.get(chat_type, "dm")


# ============================================================================
# Mentions Extraction
# ============================================================================

def extract_mentions(
    message: Message,
    bot_username: Optional[str] = None,
) -> dict[str, Any]:
    """
    Extract mentions from Telegram message
    
    Args:
        message: Telegram message
        bot_username: Bot's username (without @)
        
    Returns:
        Dict with was_mentioned flag and mention details
    """
    result = {
        "was_mentioned": False,
        "bot_username": bot_username,
        "mention_text": None,
    }
    
    if not bot_username:
        return result
    
    text = message.text or message.caption or ""
    
    # Check for @username mentions
    mention_pattern = rf"@{re.escape(bot_username)}\b"
    if re.search(mention_pattern, text, re.IGNORECASE):
        result["was_mentioned"] = True
        result["mention_text"] = f"@{bot_username}"
        return result
    
    # Check for entity mentions
    if message.entities:
        for entity in message.entities:
            if entity.type == "mention":
                mention = text[entity.offset:entity.offset + entity.length]
                if mention.lower() == f"@{bot_username.lower()}":
                    result["was_mentioned"] = True
                    result["mention_text"] = mention
                    return result
            elif entity.type == "text_mention":
                # Direct user mention (doesn't have username)
                if entity.user and hasattr(entity.user, "username"):
                    if entity.user.username and entity.user.username.lower() == bot_username.lower():
                        result["was_mentioned"] = True
                        return result
    
    return result


# ============================================================================
# Reply Context Extraction
# ============================================================================

def extract_reply_context(message: Message) -> dict[str, Optional[str]]:
    """
    Extract reply context from Telegram message
    
    Args:
        message: Telegram message
        
    Returns:
        Dict with reply_to_id and reply_to_body
    """
    if not message.reply_to_message:
        return {
            "reply_to_id": None,
            "reply_to_body": None,
        }
    
    reply_msg = message.reply_to_message
    
    return {
        "reply_to_id": str(reply_msg.message_id),
        "reply_to_body": reply_msg.text or reply_msg.caption or "",
    }


# ============================================================================
# Forward Context Extraction
# ============================================================================

def extract_forward_context(message: Message) -> dict[str, Any]:
    """
    Extract forward context from Telegram message
    
    Args:
        message: Telegram message
        
    Returns:
        Dict with forward information
    """
    if not message.forward_from and not message.forward_from_chat:
        return {"is_forwarded": False}
    
    result = {"is_forwarded": True}
    
    if message.forward_from:
        result["forward_from_user"] = message.forward_from.full_name
        result["forward_from_username"] = message.forward_from.username
    
    if message.forward_from_chat:
        result["forward_from_chat"] = message.forward_from_chat.title
        result["forward_from_chat_id"] = str(message.forward_from_chat.id)
    
    if message.forward_date:
        result["forward_date"] = message.forward_date.isoformat()
    
    return result


# ============================================================================
# Media Extraction
# ============================================================================

def extract_media_info(message: Message) -> dict[str, Any]:
    """
    Extract media information from Telegram message
    
    Args:
        message: Telegram message
        
    Returns:
        Dict with media_urls and media_type
    """
    result = {
        "media_urls": [],
        "media_type": None,
    }
    
    # Photo
    if message.photo:
        # Get largest photo
        largest = max(message.photo, key=lambda p: p.width * p.height)
        result["media_urls"].append(largest.file_id)
        result["media_type"] = "photo"
    
    # Video
    elif message.video:
        result["media_urls"].append(message.video.file_id)
        result["media_type"] = "video"
    
    # Audio
    elif message.audio:
        result["media_urls"].append(message.audio.file_id)
        result["media_type"] = "audio"
    
    # Voice
    elif message.voice:
        result["media_urls"].append(message.voice.file_id)
        result["media_type"] = "voice"
    
    # Document
    elif message.document:
        result["media_urls"].append(message.document.file_id)
        result["media_type"] = "document"
    
    # Sticker
    elif message.sticker:
        result["media_urls"].append(message.sticker.file_id)
        result["media_type"] = "sticker"
    
    return result


# ============================================================================
# Thread/Topic Handling
# ============================================================================

def extract_thread_info(message: Message) -> dict[str, Any]:
    """
    Extract thread/topic information from Telegram message
    
    Args:
        message: Telegram message
        
    Returns:
        Dict with thread_id and thread_name
    """
    result = {
        "thread_id": None,
        "thread_name": None,
    }
    
    # Telegram forum topics
    if hasattr(message, "message_thread_id") and message.message_thread_id:
        result["thread_id"] = message.message_thread_id
    
    if hasattr(message, "forum_topic_created") and message.forum_topic_created:
        result["thread_name"] = message.forum_topic_created.name
    
    return result


# ============================================================================
# Session Key Building
# ============================================================================

def build_session_key_for_telegram(
    message: Message,
    agent_id: str,
    chat_type: str,
) -> str:
    """
    Build session key for Telegram message
    
    Args:
        message: Telegram message
        agent_id: Agent identifier
        chat_type: Resolved chat type
        
    Returns:
        Session key
    """
    chat = message.chat
    thread_info = extract_thread_info(message)
    
    # Determine peer ID based on chat type
    if chat_type == "dm":
        peer_id = str(message.from_user.id) if message.from_user else str(chat.id)
    else:
        peer_id = str(chat.id)
    
    # Build session key
    session_key = build_session_key_from_context(
        agent_id=agent_id,
        channel="telegram",
        chat_type=chat_type,
        peer_id=peer_id,
        thread_id=thread_info["thread_id"],
    )
    
    return session_key


# ============================================================================
# Group History Context
# ============================================================================

def build_group_history_context(
    message: Message,
    max_history: int = 5,
) -> list[str]:
    """
    Build group history context (placeholder)
    
    In the full implementation, this would fetch recent group messages
    to provide context for the agent.
    
    Args:
        message: Telegram message
        max_history: Maximum history messages to include
        
    Returns:
        List of context strings
    """
    # Placeholder - would need to track group history
    # For now, just include reply context if present
    context = []
    
    if message.reply_to_message:
        reply_text = message.reply_to_message.text or message.reply_to_message.caption
        if reply_text:
            sender = message.reply_to_message.from_user
            sender_name = sender.full_name if sender else "Unknown"
            context.append(f"[Reply to {sender_name}]: {reply_text[:100]}")
    
    return context


# ============================================================================
# Mention Gating
# ============================================================================

def apply_mention_gating(
    ctx: MsgContext,
    group_activation_mode: str = "mention",
) -> bool:
    """
    Apply mention gating for group messages
    
    Args:
        ctx: Message context
        group_activation_mode: "mention" (require mention) or "always"
        
    Returns:
        True if message should be processed, False if should be ignored
    """
    # DMs always process
    if ctx.ChatType == "dm":
        return True
    
    # Always mode processes all messages
    if group_activation_mode == "always":
        return True
    
    # Mention mode requires bot to be mentioned
    if group_activation_mode == "mention":
        return ctx.WasMentioned
    
    # Default: require mention
    return ctx.WasMentioned


# ============================================================================
# Command Authorization
# ============================================================================

def check_command_authorization(
    message: Message,
    owner_id: Optional[str] = None,
    allowed_user_ids: Optional[list[str]] = None,
) -> bool:
    """
    Check if user is authorized to run commands
    
    Args:
        message: Telegram message
        owner_id: Owner user ID
        allowed_user_ids: List of allowed user IDs
        
    Returns:
        True if authorized
    """
    if not message.from_user:
        return False
    
    user_id = str(message.from_user.id)
    
    # Owner is always authorized
    if owner_id and user_id == owner_id:
        return True
    
    # Check allowed list
    if allowed_user_ids and user_id in allowed_user_ids:
        return True
    
    # Default: not authorized
    return False


# ============================================================================
# Main Context Builder
# ============================================================================

def build_telegram_message_context(
    update: Update,
    agent_id: str,
    bot_username: Optional[str] = None,
    owner_id: Optional[str] = None,
    allowed_user_ids: Optional[list[str]] = None,
    group_activation_mode: str = "mention",
) -> Optional[MsgContext]:
    """
    Build complete message context from Telegram update
    
    This is the main entry point for Telegram message context building.
    It extracts all relevant information and applies all normalizations.
    
    Args:
        update: Telegram update
        agent_id: Agent identifier
        bot_username: Bot's username (without @)
        owner_id: Owner user ID for command authorization
        allowed_user_ids: List of allowed user IDs
        group_activation_mode: "mention" or "always"
        
    Returns:
        Finalized message context, or None if message should be ignored
    """
    message = update.message or update.edited_message
    if not message:
        logger.warning("No message in update")
        return None
    
    # Extract sender info
    sender_info = extract_sender_info(message)
    if not sender_info["sender_id"]:
        logger.warning("No sender in message")
        return None
    
    # Resolve chat type
    chat_type = resolve_telegram_chat_type(message.chat)
    
    # Extract mentions
    mention_info = extract_mentions(message, bot_username)
    
    # Extract reply context
    reply_info = extract_reply_context(message)
    
    # Extract forward context
    forward_info = extract_forward_context(message)
    
    # Extract media
    media_info = extract_media_info(message)
    
    # Extract thread info
    thread_info = extract_thread_info(message)
    
    # Build session key
    session_key = build_session_key_for_telegram(message, agent_id, chat_type)
    
    # Get message text
    text = message.text or message.caption or ""
    
    # Build base context
    ctx = MsgContext(
        Body=text,
        RawBody=text,
        SessionKey=session_key,
        From=sender_info["sender_id"],
        To=bot_username,
        ChatType=chat_type,
        SenderName=sender_info["sender_name"],
        SenderUsername=sender_info["sender_username"],
        WasMentioned=mention_info["was_mentioned"],
        CommandAuthorized=check_command_authorization(message, owner_id, allowed_user_ids),
        ReplyToId=reply_info["reply_to_id"],
        ReplyToBody=reply_info["reply_to_body"],
        MediaUrls=media_info["media_urls"] if media_info["media_urls"] else None,
        MessageId=str(message.message_id),
        Timestamp=message.date.isoformat() if message.date else None,
        Channel="telegram",
        GroupId=str(message.chat.id) if chat_type in ["group", "channel"] else None,
        GroupName=message.chat.title if chat_type in ["group", "channel"] else None,
        TopicId=thread_info["thread_id"],
        TopicName=thread_info["thread_name"],
        OriginatingChannel="telegram",
        OriginatingTo=bot_username,
    )
    
    # Add group history context for group messages
    if chat_type in ["group", "channel"]:
        group_history = build_group_history_context(message)
        if group_history:
            ctx.UntrustedContext = group_history
    
    # Apply mention gating
    should_process = apply_mention_gating(ctx, group_activation_mode)
    if not should_process:
        logger.debug(f"Message ignored due to mention gating: {message.message_id}")
        return None
    
    # Finalize context
    finalized = finalize_inbound_context(ctx)
    
    return finalized
