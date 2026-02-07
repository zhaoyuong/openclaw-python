"""
Session ID generation and validation

Matches TypeScript patterns for session IDs.
"""

from __future__ import annotations

import re
import uuid

# Session ID regex (UUID v4 format, matches TS sessions-helpers.ts line 114)
SESSION_ID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    re.IGNORECASE,
)


def generate_session_id() -> str:
    """
    Generate a new session ID (UUID v4).

    Matches TypeScript: `crypto.randomUUID()`

    Returns:
        UUID v4 string (e.g., "550e8400-e29b-41d4-a716-446655440000")
    """
    return str(uuid.uuid4())


def looks_like_session_id(value: str | None) -> bool:
    """
    Check if value looks like a session ID (UUID format).

    Matches TS sessions-helpers.ts:116-118:
    ```typescript
    export function looksLikeSessionId(value: string | undefined): boolean {
      return !!value && SESSION_ID_RE.test(value);
    }
    ```

    Args:
        value: String to check

    Returns:
        True if value matches UUID v4 format
    """
    if not value:
        return False
    return bool(SESSION_ID_RE.match(value.strip()))


# ──────────────────────────────────────────────────────────────────────
# Session slug generation (word-based IDs, not yet in TS but planned)
# ──────────────────────────────────────────────────────────────────────

_ADJECTIVES = [
    "happy",
    "clever",
    "swift",
    "bright",
    "calm",
    "bold",
    "keen",
    "wise",
    "brave",
    "kind",
    "fair",
    "cool",
    "neat",
    "pure",
]

_NOUNS = [
    "dog",
    "cat",
    "fox",
    "owl",
    "bear",
    "wolf",
    "hawk",
    "lion",
    "deer",
    "fish",
    "bird",
    "seal",
    "crab",
    "bee",
]


def generate_session_slug() -> str:
    """
    Generate a human-readable session slug.

    Format: <adjective>-<noun>-<number>
    Example: "happy-dog-42"

    This is not currently in TypeScript but is planned for easier session reference.

    Returns:
        Session slug string
    """
    import random

    adj = random.choice(_ADJECTIVES)
    noun = random.choice(_NOUNS)
    num = random.randint(10, 99)

    return f"{adj}-{noun}-{num}"
