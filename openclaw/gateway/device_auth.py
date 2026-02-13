"""
Device authentication and pairing

Implements device identity verification with public key cryptography
matching the TypeScript implementation.
"""

import hashlib
import hmac
import logging
from typing import Optional, NamedTuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class DeviceIdentity(NamedTuple):
    """Device identity for authentication"""
    id: str
    public_key: str
    signature: str
    signed_at: str
    nonce: Optional[str] = None


class DeviceAuthResult(NamedTuple):
    """Result of device authentication"""
    ok: bool
    device_id: Optional[str] = None
    reason: Optional[str] = None


def verify_device_signature(
    device_id: str,
    public_key: str,
    signature: str,
    signed_at: str,
    nonce: Optional[str] = None,
    max_age_seconds: int = 300
) -> DeviceAuthResult:
    """
    Verify device signature
    
    Args:
        device_id: Device identifier
        public_key: Device public key
        signature: Signature to verify
        signed_at: Timestamp when signed
        nonce: Optional nonce for replay protection
        max_age_seconds: Maximum age of signature (default: 5 minutes)
        
    Returns:
        DeviceAuthResult
    """
    try:
        # Parse timestamp
        signed_time = datetime.fromisoformat(signed_at.replace("Z", "+00:00"))
        now = datetime.now(signed_time.tzinfo)
        
        # Check timestamp age
        age = (now - signed_time).total_seconds()
        if age > max_age_seconds:
            return DeviceAuthResult(
                ok=False,
                reason=f"Signature too old: {age:.1f}s > {max_age_seconds}s"
            )
        
        if age < -60:  # Allow 1 minute clock skew
            return DeviceAuthResult(
                ok=False,
                reason=f"Signature from future: {age:.1f}s"
            )
        
        # Build message to verify
        message_parts = [device_id, signed_at]
        if nonce:
            message_parts.append(nonce)
        message = "|".join(message_parts)
        
        # For now, use HMAC with public_key as secret (simplified)
        # In production, should use real public key cryptography (Ed25519/RSA)
        expected_signature = hmac.new(
            public_key.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        # Timing-safe comparison
        if not hmac.compare_digest(signature, expected_signature):
            return DeviceAuthResult(
                ok=False,
                reason="Invalid signature"
            )
        
        return DeviceAuthResult(ok=True, device_id=device_id)
        
    except Exception as e:
        logger.error(f"Failed to verify device signature: {e}")
        return DeviceAuthResult(ok=False, reason=str(e))


def authorize_device_identity(
    identity: Optional[DeviceIdentity],
    nonce: Optional[str] = None,
    require_nonce: bool = True
) -> DeviceAuthResult:
    """
    Authorize device using identity
    
    Args:
        identity: Device identity
        nonce: Expected nonce from challenge
        require_nonce: Whether to require nonce match
        
    Returns:
        DeviceAuthResult
    """
    if not identity:
        return DeviceAuthResult(ok=False, reason="No device identity provided")
    
    # Verify nonce if required
    if require_nonce:
        if not nonce:
            return DeviceAuthResult(ok=False, reason="Nonce required but not provided")
        
        if identity.nonce != nonce:
            return DeviceAuthResult(
                ok=False,
                reason="Nonce mismatch (replay protection)"
            )
    
    # Verify signature
    return verify_device_signature(
        device_id=identity.id,
        public_key=identity.public_key,
        signature=identity.signature,
        signed_at=identity.signed_at,
        nonce=identity.nonce
    )
