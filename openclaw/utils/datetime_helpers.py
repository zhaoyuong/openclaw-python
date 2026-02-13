"""
DateTime helper functions for timezone-aware operations
"""

from datetime import datetime, timezone
import sys

# Python 3.9 compatibility: UTC is only available in Python 3.11+
if sys.version_info >= (3, 11):
    from datetime import UTC
else:
    UTC = timezone.utc


def utcnow() -> datetime:
    """
    Get current UTC time as timezone-aware datetime

    Replaces deprecated datetime.utcnow() with datetime.now(timezone.utc)

    Returns:
        Timezone-aware datetime in UTC
    """
    return datetime.now(UTC)


def utc_timestamp() -> str:
    """
    Get current UTC timestamp as ISO format string

    Returns:
        ISO format timestamp string
    """
    return utcnow().isoformat()
