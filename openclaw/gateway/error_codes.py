"""
Gateway error codes

Matches TypeScript src/gateway/protocol/schema/error-codes.ts
"""
from __future__ import annotations

from enum import Enum


class ErrorCode(str, Enum):
    """
    Gateway error codes (matches TS ErrorCodes).
    
    Used for structured error responses in gateway protocol.
    """
    # Connection/Auth errors
    NOT_LINKED = "NOT_LINKED"
    NOT_PAIRED = "NOT_PAIRED"
    AUTH_REQUIRED = "AUTH_REQUIRED"
    AUTH_FAILED = "AUTH_FAILED"
    HANDSHAKE_FAILED = "HANDSHAKE_FAILED"
    
    # Request errors
    INVALID_REQUEST = "INVALID_REQUEST"
    METHOD_NOT_FOUND = "METHOD_NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    
    # Agent/Runtime errors
    AGENT_TIMEOUT = "AGENT_TIMEOUT"
    AGENT_ERROR = "AGENT_ERROR"
    
    # Service errors
    UNAVAILABLE = "UNAVAILABLE"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    
    # Session errors
    SESSION_NOT_FOUND = "SESSION_NOT_FOUND"
    
    # Channel errors
    CHANNEL_NOT_FOUND = "CHANNEL_NOT_FOUND"
    CHANNEL_ERROR = "CHANNEL_ERROR"


class GatewayError(Exception):
    """Gateway error with structured error code."""
    
    def __init__(
        self,
        message: str,
        error_code: ErrorCode,
        details: dict | None = None,
    ):
        super().__init__(message)
        self.error_code = error_code
        self.details = details or {}
    
    def to_dict(self) -> dict:
        """Convert to dict for JSON response."""
        return {
            "error": self.error_code.value,
            "message": str(self),
            "details": self.details,
        }


class NotLinkedError(GatewayError):
    """Session/device not linked."""
    def __init__(self, message: str = "Not linked", details: dict | None = None):
        super().__init__(message, ErrorCode.NOT_LINKED, details)


class NotPairedError(GatewayError):
    """Device not paired."""
    def __init__(self, message: str = "Not paired", details: dict | None = None):
        super().__init__(message, ErrorCode.NOT_PAIRED, details)


class AgentTimeoutError(GatewayError):
    """Agent request timed out."""
    def __init__(self, message: str = "Agent timeout", details: dict | None = None):
        super().__init__(message, ErrorCode.AGENT_TIMEOUT, details)


class InvalidRequestError(GatewayError):
    """Invalid request format/parameters."""
    def __init__(self, message: str = "Invalid request", details: dict | None = None):
        super().__init__(message, ErrorCode.INVALID_REQUEST, details)


class UnavailableError(GatewayError):
    """Service unavailable."""
    def __init__(self, message: str = "Unavailable", details: dict | None = None):
        super().__init__(message, ErrorCode.UNAVAILABLE, details)


class AuthRequiredError(GatewayError):
    """Authentication required."""
    def __init__(self, message: str = "Authentication required", details: dict | None = None):
        super().__init__(message, ErrorCode.AUTH_REQUIRED, details)


class AuthFailedError(GatewayError):
    """Authentication failed."""
    def __init__(self, message: str = "Authentication failed", details: dict | None = None):
        super().__init__(message, ErrorCode.AUTH_FAILED, details)


class PermissionDeniedError(GatewayError):
    """Permission denied."""
    def __init__(self, message: str = "Permission denied", details: dict | None = None):
        super().__init__(message, ErrorCode.PERMISSION_DENIED, details)


class MethodNotFoundError(GatewayError):
    """Method not found."""
    def __init__(self, message: str = "Method not found", details: dict | None = None):
        super().__init__(message, ErrorCode.METHOD_NOT_FOUND, details)


def error_shape(
    code: ErrorCode | str,
    message: str,
    details: dict | None = None,
    retryable: bool = False,
    retry_after_ms: int | None = None
) -> dict:
    """
    Create standardized error shape
    
    Args:
        code: Error code
        message: Error message
        details: Additional error details
        retryable: Whether error is retryable
        retry_after_ms: Retry delay in milliseconds
        
    Returns:
        Error shape dictionary
    """
    return {
        "code": code.value if isinstance(code, ErrorCode) else code,
        "message": message,
        "details": details,
        "retryable": retryable,
        "retryAfterMs": retry_after_ms
    }
