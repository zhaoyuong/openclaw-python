"""
Tests for session key utilities

Matches TypeScript src/routing/session-key.ts
"""

from __future__ import annotations

import pytest

from openclaw.routing.session_key import (
    DEFAULT_ACCOUNT_ID,
    DEFAULT_AGENT_ID,
    DEFAULT_MAIN_KEY,
    ParsedAgentSessionKey,
    build_agent_main_session_key,
    build_agent_peer_session_key,
    is_acp_session_key,
    is_subagent_session_key,
    looks_like_session_key,
    normalize_account_id,
    normalize_agent_id,
    normalize_main_key,
    parse_agent_session_key,
    resolve_agent_id_from_session_key,
    sanitize_agent_id,
    to_agent_request_session_key,
    to_agent_store_session_key,
)


class TestNormalizeAgentId:
    """Tests for normalize_agent_id (matches TS lines 61-78)."""

    def test_empty_returns_default(self):
        assert normalize_agent_id("") == DEFAULT_AGENT_ID
        assert normalize_agent_id(None) == DEFAULT_AGENT_ID
        assert normalize_agent_id("   ") == DEFAULT_AGENT_ID

    def test_valid_lowercase(self):
        assert normalize_agent_id("main") == "main"
        assert normalize_agent_id("agent1") == "agent1"
        assert normalize_agent_id("my-agent") == "my-agent"
        assert normalize_agent_id("my_agent") == "my_agent"

    def test_uppercase_to_lowercase(self):
        assert normalize_agent_id("Main") == "main"
        assert normalize_agent_id("AGENT") == "agent"
        assert normalize_agent_id("MyAgent") == "myagent"

    def test_invalid_chars_to_dash(self):
        assert normalize_agent_id("my agent") == "my-agent"
        assert normalize_agent_id("my@agent") == "my-agent"
        assert normalize_agent_id("my.agent!") == "my-agent"

    def test_leading_trailing_dashes_removed(self):
        assert normalize_agent_id("-agent-") == "agent"
        assert normalize_agent_id("--agent--") == "agent"

    def test_max_64_chars(self):
        long_id = "a" * 100
        result = normalize_agent_id(long_id)
        assert len(result) == 64


class TestNormalizeAccountId:
    """Tests for normalize_account_id (matches TS lines 99-114)."""

    def test_empty_returns_default(self):
        assert normalize_account_id("") == DEFAULT_ACCOUNT_ID
        assert normalize_account_id(None) == DEFAULT_ACCOUNT_ID

    def test_valid_lowercase(self):
        assert normalize_account_id("account1") == "account1"

    def test_invalid_chars_to_dash(self):
        assert normalize_account_id("Account 1") == "account-1"
        assert normalize_account_id("My@Account") == "my-account"


class TestBuildAgentMainSessionKey:
    """Tests for build_agent_main_session_key (matches TS lines 117-123)."""

    def test_default_main_key(self):
        key = build_agent_main_session_key("main")
        assert key == "agent:main:main"

    def test_custom_main_key(self):
        key = build_agent_main_session_key("main", "prod")
        assert key == "agent:main:prod"

    def test_normalizes_agent_id(self):
        key = build_agent_main_session_key("My Agent")
        assert key == "agent:my-agent:main"


class TestBuildAgentPeerSessionKey:
    """Tests for build_agent_peer_session_key."""

    def test_dm_scope_main(self):
        key = build_agent_peer_session_key("main", "telegram", "dm", "user123", dm_scope="main")
        assert key == "agent:main:main"

    def test_dm_scope_per_peer(self):
        key = build_agent_peer_session_key("main", "telegram", "dm", "user123", dm_scope="per-peer")
        assert key == "agent:main:dm:user123"

    def test_dm_scope_per_channel_peer(self):
        key = build_agent_peer_session_key(
            "main", "telegram", "dm", "user123", dm_scope="per-channel-peer"
        )
        assert key == "agent:main:telegram:dm:user123"

    def test_dm_scope_per_account_channel_peer(self):
        key = build_agent_peer_session_key(
            "main", "telegram", "dm", "user123", "acc1", dm_scope="per-account-channel-peer"
        )
        assert key == "agent:main:telegram:acc1:dm:user123"

    def test_group(self):
        key = build_agent_peer_session_key("main", "telegram", "group", "456")
        assert key == "agent:main:telegram:group:456"

    def test_channel(self):
        key = build_agent_peer_session_key("main", "discord", "channel", "789")
        assert key == "agent:main:discord:channel:789"


class TestParseAgentSessionKey:
    """Tests for parse_agent_session_key."""

    def test_valid_main_key(self):
        parsed = parse_agent_session_key("agent:main:main")
        assert parsed is not None
        assert parsed.agent_id == "main"
        assert parsed.rest == "main"
        assert parsed.full_key == "agent:main:main"

    def test_valid_group_key(self):
        parsed = parse_agent_session_key("agent:myagent:telegram:group:123")
        assert parsed is not None
        assert parsed.agent_id == "myagent"
        assert parsed.rest == "telegram:group:123"

    def test_invalid_format(self):
        assert parse_agent_session_key("invalid") is None
        assert parse_agent_session_key("agent:only-two") is None
        assert parse_agent_session_key("") is None
        assert parse_agent_session_key(None) is None


class TestResolveAgentIdFromSessionKey:
    """Tests for resolve_agent_id_from_session_key."""

    def test_valid_key(self):
        agent_id = resolve_agent_id_from_session_key("agent:myagent:main")
        assert agent_id == "myagent"

    def test_invalid_key(self):
        agent_id = resolve_agent_id_from_session_key("invalid")
        assert agent_id == DEFAULT_AGENT_ID


class TestIsSubagentSessionKey:
    """Tests for is_subagent_session_key."""

    def test_subagent_key(self):
        assert is_subagent_session_key("agent:main:subagent:test")

    def test_not_subagent_key(self):
        assert not is_subagent_session_key("agent:main:telegram:group:1")
        assert not is_subagent_session_key("agent:main:main")


class TestIsAcpSessionKey:
    """Tests for is_acp_session_key."""

    def test_acp_key(self):
        assert is_acp_session_key("agent:main:acp:session1")

    def test_not_acp_key(self):
        assert not is_acp_session_key("agent:main:main")


class TestLooksLikeSessionKey:
    """Tests for looks_like_session_key."""

    def test_valid_session_keys(self):
        assert looks_like_session_key("agent:main:main")
        assert looks_like_session_key("agent:myagent:telegram:group:123")

    def test_invalid_session_keys(self):
        assert not looks_like_session_key("invalid")
        assert not looks_like_session_key("")
        assert not looks_like_session_key(None)
