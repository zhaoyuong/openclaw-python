"""Signal Message Normalization

Normalize Signal messaging targets and detect Signal IDs.
"""

from __future__ import annotations

import re


def normalize_signal_target(raw: str) -> str | None:
    """
    Normalize Signal messaging target to standard format.
    
    Returns normalized format: signal:target
    
    Args:
        raw: Raw target string
        
    Returns:
        Normalized target or None if invalid
    """
    trimmed = raw.strip()
    if not trimmed:
        return None
    
    normalized = trimmed
    
    # Remove signal: prefix if present
    if normalized.lower().startswith("signal:"):
        normalized = normalized[7:].strip()
    
    if not normalized:
        return None
    
    # Return normalized format
    return f"signal:{normalized}".lower()


def looks_like_signal_target(raw: str) -> bool:
    """
    Check if string looks like a Signal target ID.
    
    Args:
        raw: String to check
        
    Returns:
        True if looks like Signal target
    """
    trimmed = raw.strip()
    if not trimmed:
        return False
    
    # Has signal: prefix
    if re.match(r"^signal:", trimmed, re.IGNORECASE):
        return True
    
    # Phone number format with +
    if re.match(r"^\+\d{10,15}$", trimmed):
        return True
    
    return False
