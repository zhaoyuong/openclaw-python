"""
Integration tests for complete authentication and ID system
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from openclaw.agents.command_auth import resolve_command_authorization
from openclaw.agents.session import SessionManager
from openclaw.agents.session_ids import generate_session_id, looks_like_session_id
from openclaw.auth.device_pairing import DevicePairingManager
from openclaw.auth.persistent_api_keys import PersistentAPIKeyStore
from openclaw.channels.command_auth_integration import CommandAuthHandler
from openclaw.gateway.auth import AuthMode, authorize_gateway_connect
from openclaw.gateway.auth_middleware import GatewayAuthMiddleware
from openclaw.routing.session_key import (
    build_agent_main_session_key,
    build_agent_peer_session_key,
    normalize_agent_id,
    parse_agent_session_key,
)


class TestSessionIntegration:
    """Test SessionManager integration with session keys."""

    def test_session_manager_with_keys(self, tmp_path):
        """Test SessionManager with session keys."""
        manager = SessionManager(tmp_path, agent_id="test-agent")

        # Create session with peer key
        session = manager.get_or_create_session(
            channel="telegram", peer_kind="dm", peer_id="user123", dm_scope="per-peer"
        )

        assert looks_like_session_id(session.session_id)

        # Session key should be stored
        session_key = manager.get_session_key_for_id(session.session_id)
        assert session_key is not None
        assert "telegram" in session_key
        assert "user123" in session_key

        # Retrieve same session with same parameters
        session2 = manager.get_or_create_session(
            channel="telegram", peer_kind="dm", peer_id="user123", dm_scope="per-peer"
        )

        assert session2.session_id == session.session_id

    def test_session_list_by_channel(self, tmp_path):
        """Test listing sessions by channel."""
        manager = SessionManager(tmp_path, agent_id="main")

        # Create multiple sessions
        manager.get_or_create_session(channel="telegram", peer_kind="group", peer_id="1")
        manager.get_or_create_session(channel="telegram", peer_kind="group", peer_id="2")
        manager.get_or_create_session(channel="discord", peer_kind="group", peer_id="3")

        telegram_sessions = manager.list_sessions_by_channel("telegram")
        assert len(telegram_sessions) == 2

        discord_sessions = manager.list_sessions_by_channel("discord")
        assert len(discord_sessions) == 1


class TestGatewayAuthIntegration:
    """Test Gateway authentication integration."""

    def test_gateway_auth_middleware(self):
        """Test GatewayAuthMiddleware."""
        middleware = GatewayAuthMiddleware(
            auth_mode=AuthMode.TOKEN, token="test_token_123", allow_local_direct=True
        )

        # Test token auth
        is_auth, reason, metadata = middleware.authenticate_connection(
            request_token="test_token_123", client_ip="192.168.1.1"
        )
        assert is_auth
        assert metadata["auth_method"] == "token"

        # Test local direct bypass
        is_auth, reason, metadata = middleware.authenticate_connection(
            request_token="wrong_token", client_ip="127.0.0.1"
        )
        assert is_auth
        assert metadata["auth_method"] == "local-direct"

    def test_device_pairing_flow(self):
        """Test complete device pairing flow."""
        middleware = GatewayAuthMiddleware(
            auth_mode=AuthMode.TOKEN, token="gateway_token", device_pairing_enabled=True
        )

        # 1. Create pairing request
        request_id = middleware.create_device_pairing_request(
            device_id="my-iphone",
            public_key="test_pubkey",
            display_name="My iPhone",
            platform="ios",
        )

        assert request_id is not None

        # 2. List pending
        pending = middleware.list_pending_pairing_requests()
        assert len(pending) >= 1

        # 3. Approve request
        device_info = middleware.approve_pairing_request(request_id)
        assert device_info is not None
        assert device_info["device_id"] == "my-iphone"
        assert device_info["token"] is not None

        # 4. Authenticate with device token
        is_auth, reason, metadata = middleware.authenticate_connection(
            device_id="my-iphone", device_token=device_info["token"], client_ip="192.168.1.1"
        )
        assert is_auth
        assert metadata["auth_method"] == "device"


class TestCommandAuthIntegration:
    """Test command authorization integration."""

    def test_command_auth_handler(self):
        """Test CommandAuthHandler."""
        handler = CommandAuthHandler(
            owner_list=["telegram:123", "+1234567890"], enforce_owner_for_commands=True
        )

        # Test owner
        auth = handler.authorize_command(sender_id="123", channel="telegram")
        assert auth.sender_is_owner
        assert auth.is_authorized_sender

        # Test non-owner
        auth = handler.authorize_command(sender_id="456", channel="telegram")
        assert not auth.sender_is_owner
        assert not auth.is_authorized_sender

    def test_owner_permission_check(self):
        """Test owner permission checks."""
        handler = CommandAuthHandler(owner_list=["telegram:123"], enforce_owner_for_commands=True)

        # Owner check
        assert handler.is_owner("123", channel="telegram")
        assert not handler.is_owner("456", channel="telegram")

        # Require owner
        assert handler.require_owner("123", channel="telegram")

        with pytest.raises(PermissionError):
            handler.require_owner("456", channel="telegram")


class TestPersistentAPIKeys:
    """Test persistent API key storage."""

    def test_api_key_lifecycle(self, tmp_path):
        """Test complete API key lifecycle."""
        db_path = tmp_path / "api_keys.db"
        store = PersistentAPIKeyStore(db_path)

        # Create key
        raw_key = store.create_key(
            name="Test Key", permissions=["read", "write"], expires_days=30, rate_limit=100
        )

        assert raw_key.startswith("clb_")

        # Validate key
        api_key = store.validate_key(raw_key)
        assert api_key is not None
        assert api_key.name == "Test Key"
        assert "read" in api_key.permissions
        assert api_key.is_valid()

        # List keys
        keys = store.list_keys()
        assert len(keys) == 1
        assert keys[0].name == "Test Key"

        # Revoke key
        assert store.revoke_key(api_key.key_id)

        # Key should no longer validate
        api_key2 = store.validate_key(raw_key)
        assert api_key2 is None


class TestCompleteFlow:
    """Test complete authentication and session flow."""

    def test_full_user_flow(self, tmp_path):
        """Test complete user interaction flow."""
        # 1. Gateway authentication
        middleware = GatewayAuthMiddleware(
            auth_mode=AuthMode.TOKEN, token="secret123", device_pairing_enabled=True
        )

        is_auth, _, _ = middleware.authenticate_connection(
            request_token="secret123", client_ip="192.168.1.1"
        )
        assert is_auth

        # 2. Session management
        session_manager = SessionManager(tmp_path / "workspace", agent_id="main")

        session = session_manager.get_or_create_session(
            channel="telegram", peer_kind="dm", peer_id="user123", dm_scope="per-peer"
        )

        assert looks_like_session_id(session.session_id)

        # 3. Command authorization
        auth_handler = CommandAuthHandler(
            owner_list=["telegram:user123"], enforce_owner_for_commands=True
        )

        auth = auth_handler.authorize_command(sender_id="user123", channel="telegram")

        assert auth.is_authorized_sender

        # 4. Add message to session
        session.add_user_message("Hello!")
        assert len(session.messages) == 1

        # 5. Retrieve session
        session2 = session_manager.get_or_create_session(
            channel="telegram", peer_kind="dm", peer_id="user123", dm_scope="per-peer"
        )

        assert session2.session_id == session.session_id
        assert len(session2.messages) == 1


class TestIDNormalization:
    """Test ID normalization across the system."""

    def test_agent_id_normalization(self):
        """Test agent ID normalization."""
        assert normalize_agent_id("My Agent!") == "my-agent"
        assert normalize_agent_id("") == "main"
        assert normalize_agent_id("UPPER") == "upper"

    def test_session_key_parsing(self):
        """Test session key parsing."""
        key = build_agent_main_session_key("main")
        assert key == "agent:main:main"

        parsed = parse_agent_session_key(key)
        assert parsed is not None
        assert parsed.agent_id == "main"
        assert parsed.rest == "main"

    def test_peer_session_keys(self):
        """Test peer session key generation."""
        # DM
        dm_key = build_agent_peer_session_key(
            "main", "telegram", "dm", "user123", dm_scope="per-peer"
        )
        assert "dm:user123" in dm_key

        # Group
        group_key = build_agent_peer_session_key("main", "telegram", "group", "456")
        assert "group:456" in group_key
