"""Signal Channel Actions

Implements Signal-specific actions.
"""

from __future__ import annotations

from typing import Any


class SignalActions:
    """Signal channel action adapter"""
    
    provider_id: str = "signal"
    
    @staticmethod
    def list_actions(config: dict[str, Any]) -> list[str]:
        """List available actions for Signal"""
        return ["send"]
    
    @staticmethod
    def supports_buttons(config: dict[str, Any]) -> bool:
        """Check if Signal supports buttons"""
        return False
    
    @staticmethod
    async def handle_action(
        action: str,
        params: dict[str, Any],
        config: dict[str, Any],
        account_id: str | None = None
    ) -> dict[str, Any]:
        """Handle Signal action"""
        if action == "send":
            return {
                "success": True,
                "action": "send",
                "channel": "signal"
            }
        raise ValueError(f"Action {action} not supported for Signal")
