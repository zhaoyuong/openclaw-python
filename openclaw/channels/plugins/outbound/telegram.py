"""Telegram Outbound Adapter

Handles outbound message delivery for Telegram.
Matches TypeScript implementation in src/channels/plugins/outbound/telegram.ts
"""

from __future__ import annotations

from typing import Any, Literal


def parse_reply_to_message_id(reply_to_id: str | None) -> int | None:
    """Parse reply-to message ID"""
    if not reply_to_id:
        return None
    try:
        parsed = int(reply_to_id)
        return parsed if parsed != 0 else None
    except (ValueError, TypeError):
        return None


def parse_thread_id(thread_id: str | int | None) -> int | None:
    """Parse thread ID"""
    if thread_id is None:
        return None
    
    if isinstance(thread_id, int):
        return thread_id if thread_id != 0 else None
    
    if isinstance(thread_id, str):
        trimmed = thread_id.strip()
        if not trimmed:
            return None
        try:
            parsed = int(trimmed)
            return parsed if parsed != 0 else None
        except ValueError:
            return None
    
    return None


class TelegramOutboundAdapter:
    """
    Telegram outbound message adapter.
    
    Handles chunking, formatting, and delivery of outbound messages to Telegram.
    """
    
    delivery_mode: Literal["direct"] = "direct"
    chunker_mode: Literal["markdown"] = "markdown"
    text_chunk_limit: int = 4000
    
    def __init__(self, send_telegram_fn=None):
        """
        Initialize adapter.
        
        Args:
            send_telegram_fn: Optional custom Telegram send function
        """
        self.send_telegram_fn = send_telegram_fn
    
    async def send_text(
        self,
        to: str,
        text: str,
        account_id: str | None = None,
        reply_to_id: str | None = None,
        thread_id: str | int | None = None,
        **kwargs
    ) -> dict[str, Any]:
        """
        Send text message to Telegram.
        
        Args:
            to: Target chat/channel ID
            text: Message text (supports HTML)
            account_id: Optional account ID
            reply_to_id: Optional message ID to reply to
            thread_id: Optional thread/topic ID
            
        Returns:
            Result with channel, message_id, chat_id
        """
        from openclaw.telegram.send import send_message_telegram
        
        send_fn = self.send_telegram_fn or send_message_telegram
        
        reply_to_message_id = parse_reply_to_message_id(reply_to_id)
        message_thread_id = parse_thread_id(thread_id)
        
        result = await send_fn(
            to,
            text,
            verbose=False,
            text_mode="html",
            message_thread_id=message_thread_id,
            reply_to_message_id=reply_to_message_id,
            account_id=account_id,
        )
        
        return {
            "channel": "telegram",
            **result
        }
    
    async def send_media(
        self,
        to: str,
        text: str,
        media_url: str,
        account_id: str | None = None,
        reply_to_id: str | None = None,
        thread_id: str | int | None = None,
        **kwargs
    ) -> dict[str, Any]:
        """
        Send media message to Telegram.
        
        Args:
            to: Target chat/channel ID
            text: Caption text
            media_url: URL of media to send
            account_id: Optional account ID
            reply_to_id: Optional message ID to reply to
            thread_id: Optional thread/topic ID
            
        Returns:
            Result with channel, message_id, chat_id
        """
        from openclaw.telegram.send import send_message_telegram
        
        send_fn = self.send_telegram_fn or send_message_telegram
        
        reply_to_message_id = parse_reply_to_message_id(reply_to_id)
        message_thread_id = parse_thread_id(thread_id)
        
        result = await send_fn(
            to,
            text,
            verbose=False,
            media_url=media_url,
            text_mode="html",
            message_thread_id=message_thread_id,
            reply_to_message_id=reply_to_message_id,
            account_id=account_id,
        )
        
        return {
            "channel": "telegram",
            **result
        }
    
    async def send_payload(
        self,
        to: str,
        payload: dict[str, Any],
        account_id: str | None = None,
        reply_to_id: str | None = None,
        thread_id: str | int | None = None,
        **kwargs
    ) -> dict[str, Any]:
        """
        Send structured payload to Telegram.
        
        Supports buttons, multiple media, and Telegram-specific features.
        
        Args:
            to: Target chat/channel ID
            payload: Message payload with text, media_urls, channel_data
            account_id: Optional account ID
            reply_to_id: Optional message ID to reply to
            thread_id: Optional thread/topic ID
            
        Returns:
            Result with channel, message_id, chat_id
        """
        from openclaw.telegram.send import send_message_telegram
        
        send_fn = self.send_telegram_fn or send_message_telegram
        
        reply_to_message_id = parse_reply_to_message_id(reply_to_id)
        message_thread_id = parse_thread_id(thread_id)
        
        # Extract Telegram-specific data
        telegram_data = payload.get("channel_data", {}).get("telegram", {})
        buttons = telegram_data.get("buttons")
        quote_text = telegram_data.get("quote_text")
        
        text = payload.get("text", "")
        
        # Get media URLs
        media_urls = payload.get("media_urls", [])
        if not media_urls and payload.get("media_url"):
            media_urls = [payload["media_url"]]
        
        base_opts = {
            "verbose": False,
            "text_mode": "html",
            "message_thread_id": message_thread_id,
            "reply_to_message_id": reply_to_message_id,
            "quote_text": quote_text,
            "account_id": account_id,
        }
        
        # Send without media
        if not media_urls:
            result = await send_fn(
                to,
                text,
                buttons=buttons,
                **base_opts
            )
            return {
                "channel": "telegram",
                **result
            }
        
        # Send with media (attach buttons only to first message)
        final_result = None
        for i, media_url in enumerate(media_urls):
            is_first = i == 0
            result = await send_fn(
                to,
                text if is_first else "",
                media_url=media_url,
                buttons=buttons if is_first else None,
                **base_opts
            )
            final_result = result
        
        return {
            "channel": "telegram",
            **(final_result or {"message_id": "unknown", "chat_id": to})
        }
