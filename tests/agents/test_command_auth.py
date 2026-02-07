"""
Tests for command authorization

Matches TypeScript src/auto-reply/command-auth.ts
"""

from __future__ import annotations

import pytest

from openclaw.agents.command_auth import (
    CommandAuthorization,
    check_owner_permission,
    resolve_command_authorization,
    resolve_sender_candidates,
)


class TestResolveSenderCandidates:
    """Tests for resolve_sender_candidates (matches TS lines 129-165)."""

    def test_basic_candidates(self):
        candidates = resolve_sender_candidates(
            sender_id="123",
            sender_e164="+1234567890",
            from_="user@example.com",
            provider_id="telegram",
        )
        assert "telegram:123" in candidates
        assert "123" in candidates
        assert "+1234567890" in candidates
        assert "user@example.com" in candidates

    def test_only_sender_id(self):
        candidates = resolve_sender_candidates(
            sender_id="123", sender_e164=None, from_=None, provider_id="telegram"
        )
        assert "telegram:123" in candidates
        assert "123" in candidates
        assert len(candidates) == 2

    def test_no_provider_id(self):
        candidates = resolve_sender_candidates(
            sender_id="123", sender_e164=None, from_=None, provider_id=None
        )
        assert "123" in candidates
        assert "telegram:123" not in candidates

    def test_empty_inputs(self):
        candidates = resolve_sender_candidates(
            sender_id=None, sender_e164=None, from_=None, provider_id=None
        )
        assert len(candidates) == 0


class TestResolveCommandAuthorization:
    """Tests for resolve_command_authorization (matches TS lines 168-269)."""

    def test_owner_match(self):
        auth = resolve_command_authorization(
            sender_id="123",
            sender_e164=None,
            from_=None,
            to=None,
            owner_list=["telegram:123"],
            provider_id="telegram",
        )
        assert auth.sender_is_owner
        assert auth.is_authorized_sender
        assert auth.sender_id == "telegram:123"

    def test_not_owner_no_enforcement(self):
        """Not owner but no enforcement = still authorized."""
        auth = resolve_command_authorization(
            sender_id="456",
            sender_e164=None,
            from_=None,
            to=None,
            owner_list=["telegram:123"],
            enforce_owner_for_commands=False,
            provider_id="telegram",
        )
        assert not auth.sender_is_owner
        assert auth.is_authorized_sender  # No enforcement

    def test_not_owner_with_enforcement(self):
        """Not owner and enforcement = not authorized."""
        auth = resolve_command_authorization(
            sender_id="456",
            sender_e164=None,
            from_=None,
            to=None,
            owner_list=["telegram:123"],
            enforce_owner_for_commands=True,
            provider_id="telegram",
        )
        assert not auth.sender_is_owner
        assert not auth.is_authorized_sender

    def test_wildcard_owner(self):
        """Wildcard in owner list = everyone is owner."""
        auth = resolve_command_authorization(
            sender_id="anyone",
            sender_e164=None,
            from_=None,
            to=None,
            owner_list=["*"],
            provider_id="telegram",
        )
        assert auth.is_authorized_sender

    def test_empty_owner_list(self):
        """Empty owner list = no restrictions."""
        auth = resolve_command_authorization(
            sender_id="123",
            sender_e164=None,
            from_=None,
            to=None,
            owner_list=[],
            provider_id="telegram",
        )
        assert auth.is_authorized_sender

    def test_multiple_owner_candidates(self):
        """Match any candidate in owner list."""
        auth = resolve_command_authorization(
            sender_id="123",
            sender_e164="+1234567890",
            from_=None,
            to=None,
            owner_list=["+1234567890"],  # Match on E.164
            provider_id="telegram",
        )
        assert auth.sender_is_owner
        assert auth.is_authorized_sender


class TestCheckOwnerPermission:
    """Tests for check_owner_permission utility."""

    def test_owner_match(self):
        is_owner = check_owner_permission("123", None, ["telegram:123"], "telegram")
        assert is_owner

    def test_not_owner(self):
        is_owner = check_owner_permission("456", None, ["telegram:123"], "telegram")
        assert not is_owner

    def test_wildcard(self):
        is_owner = check_owner_permission("anyone", None, ["*"], "telegram")
        assert is_owner

    def test_e164_match(self):
        is_owner = check_owner_permission(None, "+1234567890", ["+1234567890"], "whatsapp")
        assert is_owner
