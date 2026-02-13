"""Discord Message Normalization

Normalize Discord messaging targets and detect Discord IDs.
"""

from __future__ import annotations

import re


def normalize_discord_target(raw: str) -> str | None:
    """
    Normalize Discord messaging target to standard format.
    
    Returns normalized format: discord:target
    
    Args:
        raw: Raw target string
        
    Returns:
        Normalized target or None if invalid
    """
    trimmed = raw.strip()
    if not trimmed:
        return None
    
    normalized = trimmed
    
    # Remove discord: prefix if present
    if normalized.lower().startswith("discord:"):
        normalized = normalized[8:].strip()
    
    if not normalized:
        return None
    
    # Return normalized format
    return f"discord:{normalized}".lower()


def looks_like_discord_target(raw: str) -> bool:
    """
    Check if string looks like a Discord target ID.
    
    Args:
        raw: String to check
        
    Returns:
        True if looks like Discord target
    """
    trimmed = raw.strip()
    if not trimmed:
        return False
    
    # Has discord: prefix
    if re.match(r"^discord:", trimmed, re.IGNORECASE):
        return True
    
    # Discord snowflake ID (17-20 digits)
    if re.match(r"^\d{17,20}$", trimmed):
        return True
    
    return False
