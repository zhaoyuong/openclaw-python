"""Channel Plugins Architecture

This module implements the plugin architecture for channel-specific functionality,
matching the TypeScript implementation in src/channels/plugins/

Plugin Types:
- actions: Channel-specific actions (send, react, delete, edit, etc.)
- agent_tools: Channel-exposed tools for agent use
- normalize: Message normalization and target ID parsing
- onboarding: Channel onboarding and setup flows
- outbound: Outbound message adapters
- status_issues: Status checking and issue reporting
"""

from __future__ import annotations

__all__ = [
    "actions",
    "agent_tools",
    "normalize",
    "onboarding",
    "outbound",
    "status_issues",
]
