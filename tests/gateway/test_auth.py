"""
Tests for gateway authentication

Matches TypeScript src/gateway/auth.ts
"""

from __future__ import annotations

import pytest

from openclaw.gateway.auth import (
    AuthMethod,
    AuthMode,
    AuthResult,
    authorize_gateway_connect,
    authorize_gateway_password,
    authorize_gateway_token,
    is_loopback_address,
    safe_equal,
    validate_auth_config,
)


class TestSafeEqual:
    """Tests for safe_equal (timing-safe comparison)."""

    def test_equal_strings(self):
        assert safe_equal("test123", "test123")
        assert safe_equal("", "")

    def test_unequal_strings(self):
        assert not safe_equal("test123", "test456")
        assert not safe_equal("test", "testing")

    def test_different_lengths(self):
        assert not safe_equal("short", "longer")
        assert not safe_equal("", "nonempty")


class TestIsLoopbackAddress:
    """Tests for is_loopback_address (matches TS lines 46-62)."""

    def test_loopback_ipv4(self):
        assert is_loopback_address("127.0.0.1")
        assert is_loopback_address("127.0.5.1")
        assert is_loopback_address("127.255.255.255")

    def test_loopback_ipv6(self):
        assert is_loopback_address("::1")
        assert is_loopback_address("::ffff:127.0.0.1")

    def test_non_loopback(self):
        assert not is_loopback_address("192.168.1.1")
        assert not is_loopback_address("10.0.0.1")
        assert not is_loopback_address("8.8.8.8")

    def test_empty_or_none(self):
        assert not is_loopback_address("")
        assert not is_loopback_address(None)


class TestAuthorizeGatewayToken:
    """Tests for authorize_gateway_token (matches TS lines 263-273)."""

    def test_success(self):
        result = authorize_gateway_token("token123", "token123")
        assert result.ok
        assert result.method == AuthMethod.TOKEN
        assert result.reason is None

    def test_token_mismatch(self):
        result = authorize_gateway_token("token123", "wrong")
        assert not result.ok
        assert result.reason == "token_mismatch"

    def test_token_missing(self):
        result = authorize_gateway_token("token123", None)
        assert not result.ok
        assert result.reason == "token_missing"

    def test_config_token_missing(self):
        result = authorize_gateway_token(None, "token123")
        assert not result.ok
        assert result.reason == "token_missing_config"


class TestAuthorizeGatewayPassword:
    """Tests for authorize_gateway_password (matches TS lines 276-287)."""

    def test_success(self):
        result = authorize_gateway_password("pass123", "pass123")
        assert result.ok
        assert result.method == AuthMethod.PASSWORD

    def test_password_mismatch(self):
        result = authorize_gateway_password("pass123", "wrong")
        assert not result.ok
        assert result.reason == "password_mismatch"

    def test_password_missing(self):
        result = authorize_gateway_password("pass123", None)
        assert not result.ok
        assert result.reason == "password_missing"


class TestAuthorizeGatewayConnect:
    """Tests for authorize_gateway_connect (main entry point)."""

    def test_token_mode_success(self):
        result = authorize_gateway_connect(
            auth_mode=AuthMode.TOKEN,
            config_token="token123",
            request_token="token123",
            client_ip="192.168.1.1",
        )
        assert result.ok
        assert result.method == AuthMethod.TOKEN

    def test_password_mode_success(self):
        result = authorize_gateway_connect(
            auth_mode=AuthMode.PASSWORD,
            config_password="pass123",
            request_password="pass123",
            client_ip="192.168.1.1",
        )
        assert result.ok
        assert result.method == AuthMethod.PASSWORD

    def test_local_direct_bypass(self):
        """Local connections bypass auth."""
        result = authorize_gateway_connect(
            auth_mode=AuthMode.TOKEN,
            config_token="token123",
            request_token="wrong",  # Wrong token
            client_ip="127.0.0.1",  # But local
        )
        assert result.ok
        assert result.method == AuthMethod.LOCAL_DIRECT

    def test_unauthorized(self):
        result = authorize_gateway_connect(
            auth_mode=AuthMode.TOKEN,
            config_token="token123",
            request_token="wrong",
            client_ip="192.168.1.1",
        )
        assert not result.ok


class TestValidateAuthConfig:
    """Tests for validate_auth_config (matches TS lines 225-235)."""

    def test_token_mode_valid(self):
        # Should not raise
        validate_auth_config(AuthMode.TOKEN, "token123", None)

    def test_token_mode_missing(self):
        with pytest.raises(ValueError, match="no token was configured"):
            validate_auth_config(AuthMode.TOKEN, None, None)

    def test_password_mode_valid(self):
        # Should not raise
        validate_auth_config(AuthMode.PASSWORD, None, "pass123")

    def test_password_mode_missing(self):
        with pytest.raises(ValueError, match="no password was configured"):
            validate_auth_config(AuthMode.PASSWORD, None, None)
