"""
Tests for session ID generation

Matches TypeScript session ID patterns
"""

from __future__ import annotations

import pytest

from openclaw.agents.session_ids import (
    generate_session_id,
    generate_session_slug,
    looks_like_session_id,
)


class TestGenerateSessionId:
    """Tests for generate_session_id."""

    def test_generates_valid_uuid(self):
        sid = generate_session_id()
        assert looks_like_session_id(sid)

    def test_generates_unique_ids(self):
        ids = [generate_session_id() for _ in range(10)]
        assert len(set(ids)) == 10  # All unique


class TestLooksLikeSessionId:
    """Tests for looks_like_session_id (matches TS lines 116-118)."""

    def test_valid_uuids(self):
        assert looks_like_session_id("550e8400-e29b-41d4-a716-446655440000")
        assert looks_like_session_id("123e4567-e89b-12d3-a456-426614174000")
        assert looks_like_session_id("AAAAAAAA-BBBB-CCCC-DDDD-EEEEEEEEEEEE")

    def test_invalid_formats(self):
        assert not looks_like_session_id("not-a-uuid")
        assert not looks_like_session_id("123-456")
        assert not looks_like_session_id("")
        assert not looks_like_session_id(None)
        assert not looks_like_session_id("550e8400-e29b-41d4-a716")  # Too short

    def test_case_insensitive(self):
        assert looks_like_session_id("550e8400-e29b-41d4-a716-446655440000")
        assert looks_like_session_id("550E8400-E29B-41D4-A716-446655440000")


class TestGenerateSessionSlug:
    """Tests for generate_session_slug."""

    def test_format(self):
        slug = generate_session_slug()
        parts = slug.split("-")
        assert len(parts) == 3  # adjective-noun-number
        assert parts[2].isdigit()

    def test_generates_varied_slugs(self):
        slugs = [generate_session_slug() for _ in range(20)]
        # Should have some variety (not all identical)
        assert len(set(slugs)) > 1
