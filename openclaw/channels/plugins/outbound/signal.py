"""Signal Outbound Adapter

Handles outbound message delivery for Signal.
"""

from __future__ import annotations

from typing import Any, Literal


class SignalOutboundAdapter:
    """Signal outbound message adapter"""
    
    delivery_mode: Literal["direct"] = "direct"
    chunker_mode: Literal["plain"] = "plain"
    text_chunk_limit: int = 2000
    
    async def send_text(
        self,
        to: str,
        text: str,
        account_id: str | None = None,
        **kwargs
    ) -> dict[str, Any]:
        """Send text message to Signal"""
        return {
            "channel": "signal",
            "message_id": "pending",
            "recipient": to
        }
    
    async def send_media(
        self,
        to: str,
        text: str,
        media_url: str,
        account_id: str | None = None,
        **kwargs
    ) -> dict[str, Any]:
        """Send media message to Signal"""
        return {
            "channel": "signal",
            "message_id": "pending",
            "recipient": to
        }
    
    async def send_payload(
        self,
        to: str,
        payload: dict[str, Any],
        account_id: str | None = None,
        **kwargs
    ) -> dict[str, Any]:
        """Send structured payload to Signal"""
        return {
            "channel": "signal",
            "message_id": "pending",
            "recipient": to
        }
