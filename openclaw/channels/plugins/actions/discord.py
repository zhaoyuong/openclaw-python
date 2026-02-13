"""Discord Channel Actions

Implements Discord-specific actions.
"""

from __future__ import annotations

from typing import Any


class DiscordActions:
    """Discord channel action adapter"""
    
    provider_id: str = "discord"
    
    @staticmethod
    def list_actions(config: dict[str, Any]) -> list[str]:
        """List available actions for Discord"""
        return ["send"]
    
    @staticmethod
    def supports_buttons(config: dict[str, Any]) -> bool:
        """Check if Discord supports buttons"""
        return True
    
    @staticmethod
    async def handle_action(
        action: str,
        params: dict[str, Any],
        config: dict[str, Any],
        account_id: str | None = None
    ) -> dict[str, Any]:
        """Handle Discord action"""
        if action == "send":
            return {
                "success": True,
                "action": "send",
                "channel": "discord"
            }
        raise ValueError(f"Action {action} not supported for Discord")
