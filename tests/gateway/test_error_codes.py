"""
Tests for gateway error codes

Matches TypeScript src/gateway/protocol/schema/error-codes.ts
"""

from __future__ import annotations

import pytest

from openclaw.gateway.error_codes import (
    AgentTimeoutError,
    ErrorCode,
    GatewayError,
    InvalidRequestError,
    NotLinkedError,
    NotPairedError,
    UnavailableError,
)


class TestErrorCode:
    """Tests for ErrorCode enum."""

    def test_all_codes(self):
        assert ErrorCode.NOT_LINKED == "NOT_LINKED"
        assert ErrorCode.NOT_PAIRED == "NOT_PAIRED"
        assert ErrorCode.AGENT_TIMEOUT == "AGENT_TIMEOUT"
        assert ErrorCode.INVALID_REQUEST == "INVALID_REQUEST"
        assert ErrorCode.UNAVAILABLE == "UNAVAILABLE"


class TestGatewayError:
    """Tests for GatewayError base class."""

    def test_basic_error(self):
        err = GatewayError("Test error", ErrorCode.INVALID_REQUEST)
        assert str(err) == "Test error"
        assert err.error_code == ErrorCode.INVALID_REQUEST
        assert err.details == {}

    def test_with_details(self):
        err = GatewayError("Test error", ErrorCode.INVALID_REQUEST, {"field": "value"})
        assert err.details == {"field": "value"}

    def test_to_dict(self):
        err = GatewayError("Test error", ErrorCode.INVALID_REQUEST, {"field": "value"})
        d = err.to_dict()
        assert d["error"] == "INVALID_REQUEST"
        assert d["message"] == "Test error"
        assert d["details"] == {"field": "value"}


class TestSpecificErrors:
    """Tests for specific error classes."""

    def test_not_linked_error(self):
        err = NotLinkedError()
        assert err.error_code == ErrorCode.NOT_LINKED
        assert "Not linked" in str(err)

    def test_not_paired_error(self):
        err = NotPairedError("Device not found")
        assert err.error_code == ErrorCode.NOT_PAIRED
        assert str(err) == "Device not found"

    def test_agent_timeout_error(self):
        err = AgentTimeoutError()
        assert err.error_code == ErrorCode.AGENT_TIMEOUT

    def test_invalid_request_error(self):
        err = InvalidRequestError("Bad param")
        assert err.error_code == ErrorCode.INVALID_REQUEST

    def test_unavailable_error(self):
        err = UnavailableError()
        assert err.error_code == ErrorCode.UNAVAILABLE
