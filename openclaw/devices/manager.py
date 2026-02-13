"""
Device management service

Manages device pairing, tokens, and authentication.
"""

import logging
import secrets
import time
from typing import Any, Dict, Optional, List
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class Device:
    """Device information"""
    id: str
    public_key: str
    paired_at: float = field(default_factory=time.time)
    last_seen: float = field(default_factory=time.time)
    label: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DevicePairRequest:
    """Device pairing request"""
    device_id: str
    public_key: str
    requested_at: float = field(default_factory=time.time)
    status: str = "pending"  # pending | approved | rejected


@dataclass
class DeviceToken:
    """Device access token"""
    token: str
    device_id: str
    created_at: float = field(default_factory=time.time)
    expires_at: Optional[float] = None
    revoked: bool = False


class DeviceManager:
    """
    Device management service
    
    Handles:
    - Device pairing
    - Token generation and management
    - Device authentication
    """
    
    def __init__(self):
        """Initialize device manager"""
        self.devices: Dict[str, Device] = {}
        self.pending_pairs: Dict[str, DevicePairRequest] = {}
        self.tokens: Dict[str, DeviceToken] = {}
    
    def request_pairing(
        self,
        device_id: str,
        public_key: str
    ) -> DevicePairRequest:
        """
        Request device pairing
        
        Args:
            device_id: Device identifier
            public_key: Device public key
            
        Returns:
            DevicePairRequest
        """
        request = DevicePairRequest(
            device_id=device_id,
            public_key=public_key
        )
        
        self.pending_pairs[device_id] = request
        logger.info(f"Device pairing requested: {device_id}")
        
        # TODO: Broadcast device.pair.requested event
        
        return request
    
    def approve_pairing(
        self,
        device_id: str,
        label: Optional[str] = None
    ) -> Optional[str]:
        """
        Approve device pairing
        
        Args:
            device_id: Device identifier
            label: Optional device label
            
        Returns:
            Device token or None if request not found
        """
        request = self.pending_pairs.get(device_id)
        if not request:
            logger.warning(f"No pending pair request for device: {device_id}")
            return None
        
        # Create device
        device = Device(
            id=device_id,
            public_key=request.public_key,
            label=label
        )
        self.devices[device_id] = device
        
        # Generate token
        token = secrets.token_urlsafe(32)
        device_token = DeviceToken(
            token=token,
            device_id=device_id
        )
        self.tokens[token] = device_token
        
        # Update request status
        request.status = "approved"
        
        # Remove from pending
        del self.pending_pairs[device_id]
        
        logger.info(f"Device pairing approved: {device_id}")
        
        # TODO: Broadcast device.pair.resolved event
        
        return token
    
    def reject_pairing(
        self,
        device_id: str,
        reason: Optional[str] = None
    ):
        """
        Reject device pairing
        
        Args:
            device_id: Device identifier
            reason: Rejection reason
        """
        request = self.pending_pairs.get(device_id)
        if not request:
            logger.warning(f"No pending pair request for device: {device_id}")
            return
        
        request.status = "rejected"
        
        # Remove from pending
        del self.pending_pairs[device_id]
        
        logger.info(f"Device pairing rejected: {device_id}, reason: {reason}")
        
        # TODO: Broadcast device.pair.rejected event
    
    def list_devices(self) -> List[Dict[str, Any]]:
        """
        List all paired devices
        
        Returns:
            List of device info dictionaries
        """
        devices = []
        for device in self.devices.values():
            devices.append({
                "id": device.id,
                "label": device.label,
                "pairedAt": device.paired_at,
                "lastSeen": device.last_seen,
                "metadata": device.metadata
            })
        return devices
    
    def list_pending_pairs(self) -> List[Dict[str, Any]]:
        """
        List pending pairing requests
        
        Returns:
            List of pending pair requests
        """
        pairs = []
        for request in self.pending_pairs.values():
            pairs.append({
                "deviceId": request.device_id,
                "requestedAt": request.requested_at,
                "status": request.status
            })
        return pairs
    
    def get_device(self, device_id: str) -> Optional[Device]:
        """
        Get device by ID
        
        Args:
            device_id: Device identifier
            
        Returns:
            Device or None
        """
        return self.devices.get(device_id)
    
    def verify_token(self, token: str) -> Optional[str]:
        """
        Verify device token
        
        Args:
            token: Device token
            
        Returns:
            Device ID or None if invalid
        """
        device_token = self.tokens.get(token)
        if not device_token:
            return None
        
        if device_token.revoked:
            return None
        
        # Check expiration
        if device_token.expires_at and time.time() > device_token.expires_at:
            return None
        
        return device_token.device_id
    
    def rotate_token(self, device_id: str) -> Optional[str]:
        """
        Rotate device token
        
        Args:
            device_id: Device identifier
            
        Returns:
            New token or None if device not found
        """
        device = self.devices.get(device_id)
        if not device:
            logger.warning(f"Device not found: {device_id}")
            return None
        
        # Revoke old tokens
        for token, device_token in self.tokens.items():
            if device_token.device_id == device_id:
                device_token.revoked = True
        
        # Generate new token
        new_token = secrets.token_urlsafe(32)
        device_token = DeviceToken(
            token=new_token,
            device_id=device_id
        )
        self.tokens[new_token] = device_token
        
        logger.info(f"Device token rotated: {device_id}")
        
        return new_token
    
    def revoke_token(self, token: str) -> bool:
        """
        Revoke device token
        
        Args:
            token: Device token
            
        Returns:
            True if successful
        """
        device_token = self.tokens.get(token)
        if not device_token:
            return False
        
        device_token.revoked = True
        logger.info(f"Device token revoked for device: {device_token.device_id}")
        
        return True


# Global device manager instance
_device_manager: Optional[DeviceManager] = None


def get_device_manager() -> DeviceManager:
    """Get global device manager instance"""
    global _device_manager
    if _device_manager is None:
        _device_manager = DeviceManager()
    return _device_manager


def set_device_manager(manager: DeviceManager):
    """Set global device manager instance"""
    global _device_manager
    _device_manager = manager
