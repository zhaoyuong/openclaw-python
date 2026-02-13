"""Telegram Message Normalization

Normalize Telegram messaging targets and detect Telegram IDs.
Matches TypeScript implementation in src/channels/plugins/normalize/telegram.ts
"""

from __future__ import annotations

import re


def normalize_telegram_target(raw: str) -> str | None:
    """
    Normalize Telegram messaging target to standard format.
    
    Accepts:
    - telegram:username or telegram:@username
    - tg:username or tg:@username
    - @username
    - https://t.me/username or t.me/username
    - Chat ID (numeric)
    
    Returns normalized format: telegram:target (lowercase)
    
    Args:
        raw: Raw target string
        
    Returns:
        Normalized target or None if invalid
        
    Example:
        >>> normalize_telegram_target("@username")
        'telegram:@username'
        >>> normalize_telegram_target("https://t.me/username")
        'telegram:@username'
        >>> normalize_telegram_target("telegram:@username")
        'telegram:@username'
    """
    trimmed = raw.strip()
    if not trimmed:
        return None
    
    normalized = trimmed
    
    # Remove telegram: or tg: prefix
    if normalized.lower().startswith("telegram:"):
        normalized = normalized[9:].strip()
    elif normalized.lower().startswith("tg:"):
        normalized = normalized[3:].strip()
    
    if not normalized:
        return None
    
    # Parse t.me URLs
    # https://t.me/username or t.me/username
    tme_match = re.match(
        r"^https?://t\.me/([A-Za-z0-9_]+)$", 
        normalized,
        re.IGNORECASE
    )
    if not tme_match:
        tme_match = re.match(
            r"^t\.me/([A-Za-z0-9_]+)$",
            normalized,
            re.IGNORECASE
        )
    
    if tme_match:
        normalized = f"@{tme_match.group(1)}"
    
    if not normalized:
        return None
    
    # Return normalized format
    return f"telegram:{normalized}".lower()


def looks_like_telegram_target(raw: str) -> bool:
    """
    Check if string looks like a Telegram target ID.
    
    Args:
        raw: String to check
        
    Returns:
        True if looks like Telegram target
        
    Example:
        >>> looks_like_telegram_target("@username")
        True
        >>> looks_like_telegram_target("telegram:123456")
        True
        >>> looks_like_telegram_target("-1001234567890")
        True
        >>> looks_like_telegram_target("random text")
        False
    """
    trimmed = raw.strip()
    if not trimmed:
        return False
    
    # Has telegram: or tg: prefix
    if re.match(r"^(telegram|tg):", trimmed, re.IGNORECASE):
        return True
    
    # Starts with @
    if trimmed.startswith("@"):
        return True
    
    # Numeric ID (at least 6 digits, can be negative for groups)
    if re.match(r"^-?\d{6,}$", trimmed):
        return True
    
    return False
