"""Discord Outbound Adapter

Handles outbound message delivery for Discord.
"""

from __future__ import annotations

from typing import Any, Literal


class DiscordOutboundAdapter:
    """Discord outbound message adapter"""
    
    delivery_mode: Literal["direct"] = "direct"
    chunker_mode: Literal["markdown"] = "markdown"
    text_chunk_limit: int = 2000
    
    async def send_text(
        self,
        to: str,
        text: str,
        account_id: str | None = None,
        **kwargs
    ) -> dict[str, Any]:
        """Send text message to Discord"""
        # Implementation would call Discord API
        return {
            "channel": "discord",
            "message_id": "pending",
            "channel_id": to
        }
    
    async def send_media(
        self,
        to: str,
        text: str,
        media_url: str,
        account_id: str | None = None,
        **kwargs
    ) -> dict[str, Any]:
        """Send media message to Discord"""
        return {
            "channel": "discord",
            "message_id": "pending",
            "channel_id": to
        }
    
    async def send_payload(
        self,
        to: str,
        payload: dict[str, Any],
        account_id: str | None = None,
        **kwargs
    ) -> dict[str, Any]:
        """Send structured payload to Discord"""
        return {
            "channel": "discord",
            "message_id": "pending",
            "channel_id": to
        }
