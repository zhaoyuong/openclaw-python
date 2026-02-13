"""Slack Message Normalization

Normalize Slack messaging targets and detect Slack IDs.
"""

from __future__ import annotations

import re


def normalize_slack_target(raw: str) -> str | None:
    """
    Normalize Slack messaging target to standard format.
    
    Returns normalized format: slack:target
    
    Args:
        raw: Raw target string
        
    Returns:
        Normalized target or None if invalid
    """
    trimmed = raw.strip()
    if not trimmed:
        return None
    
    normalized = trimmed
    
    # Remove slack: prefix if present
    if normalized.lower().startswith("slack:"):
        normalized = normalized[6:].strip()
    
    if not normalized:
        return None
    
    # Return normalized format
    return f"slack:{normalized}".lower()


def looks_like_slack_target(raw: str) -> bool:
    """
    Check if string looks like a Slack target ID.
    
    Args:
        raw: String to check
        
    Returns:
        True if looks like Slack target
    """
    trimmed = raw.strip()
    if not trimmed:
        return False
    
    # Has slack: prefix
    if re.match(r"^slack:", trimmed, re.IGNORECASE):
        return True
    
    # Slack channel ID format (starts with C, D, or G)
    if re.match(r"^[CDG][A-Z0-9]{8,}$", trimmed):
        return True
    
    return False
