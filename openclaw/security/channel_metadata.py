"""Channel security metadata management

This module manages security metadata for different channels including:
- Channel permissions
- User authentication levels
- Rate limiting
- Security policies per channel
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Literal

logger = logging.getLogger(__name__)


@dataclass
class ChannelPermissions:
    """Permissions for a channel"""
    
    allow_file_read: bool = True
    allow_file_write: bool = False
    allow_file_delete: bool = False
    allow_command_execution: bool = False
    allow_browser_access: bool = False
    allow_network_access: bool = True
    allow_subagent_spawn: bool = True
    allowed_tools: list[str] = field(default_factory=list)  # Empty = all allowed
    blocked_tools: list[str] = field(default_factory=list)
    
    def is_tool_allowed(self, tool_name: str) -> bool:
        """
        Check if tool is allowed
        
        Args:
            tool_name: Tool name to check
            
        Returns:
            True if allowed
        """
        # If blocked list has items, check it first
        if self.blocked_tools and tool_name in self.blocked_tools:
            return False
        
        # If allowed list is empty, all tools allowed (except blocked)
        if not self.allowed_tools:
            return True
        
        # Check allowed list
        return tool_name in self.allowed_tools


@dataclass
class RateLimitConfig:
    """Rate limiting configuration"""
    
    max_messages_per_minute: int = 60
    max_messages_per_hour: int = 500
    max_tokens_per_day: int = 100000
    max_file_operations_per_hour: int = 100
    max_command_executions_per_hour: int = 50
    
    def __post_init__(self):
        """Validate configuration"""
        if self.max_messages_per_minute <= 0:
            raise ValueError("max_messages_per_minute must be positive")
        if self.max_messages_per_hour <= 0:
            raise ValueError("max_messages_per_hour must be positive")


@dataclass
class ChannelSecurityMetadata:
    """Security metadata for a channel"""
    
    channel_id: str
    channel_type: str  # telegram, discord, slack, etc.
    auth_level: Literal["public", "authenticated", "admin"] = "authenticated"
    permissions: ChannelPermissions = field(default_factory=ChannelPermissions)
    rate_limit: RateLimitConfig = field(default_factory=RateLimitConfig)
    require_approval_for_destructive: bool = True
    require_approval_for_sensitive: bool = True
    audit_all_operations: bool = True
    allowed_domains: list[str] = field(default_factory=list)  # Empty = all allowed
    blocked_domains: list[str] = field(default_factory=list)
    max_file_size_mb: int = 10
    max_session_duration_hours: int = 24
    
    def is_domain_allowed(self, domain: str) -> bool:
        """
        Check if domain is allowed
        
        Args:
            domain: Domain to check
            
        Returns:
            True if allowed
        """
        domain = domain.lower()
        
        # Check blocked list first
        if any(blocked in domain for blocked in self.blocked_domains):
            return False
        
        # If allowed list is empty, all domains allowed
        if not self.allowed_domains:
            return True
        
        # Check allowed list
        return any(allowed in domain for allowed in self.allowed_domains)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary"""
        return {
            "channel_id": self.channel_id,
            "channel_type": self.channel_type,
            "auth_level": self.auth_level,
            "permissions": {
                "allow_file_read": self.permissions.allow_file_read,
                "allow_file_write": self.permissions.allow_file_write,
                "allow_file_delete": self.permissions.allow_file_delete,
                "allow_command_execution": self.permissions.allow_command_execution,
                "allow_browser_access": self.permissions.allow_browser_access,
                "allow_network_access": self.permissions.allow_network_access,
                "allow_subagent_spawn": self.permissions.allow_subagent_spawn,
                "allowed_tools": self.permissions.allowed_tools,
                "blocked_tools": self.permissions.blocked_tools,
            },
            "rate_limit": {
                "max_messages_per_minute": self.rate_limit.max_messages_per_minute,
                "max_messages_per_hour": self.rate_limit.max_messages_per_hour,
                "max_tokens_per_day": self.rate_limit.max_tokens_per_day,
                "max_file_operations_per_hour": self.rate_limit.max_file_operations_per_hour,
                "max_command_executions_per_hour": self.rate_limit.max_command_executions_per_hour,
            },
            "require_approval_for_destructive": self.require_approval_for_destructive,
            "require_approval_for_sensitive": self.require_approval_for_sensitive,
            "audit_all_operations": self.audit_all_operations,
            "allowed_domains": self.allowed_domains,
            "blocked_domains": self.blocked_domains,
            "max_file_size_mb": self.max_file_size_mb,
            "max_session_duration_hours": self.max_session_duration_hours,
        }


class ChannelSecurityManager:
    """Manager for channel security metadata"""
    
    def __init__(self):
        """Initialize security manager"""
        self.channels: dict[str, ChannelSecurityMetadata] = {}
        self._load_defaults()
    
    def _load_defaults(self) -> None:
        """Load default security profiles"""
        # Public channel (most restrictive)
        self.channels["default_public"] = ChannelSecurityMetadata(
            channel_id="default_public",
            channel_type="public",
            auth_level="public",
            permissions=ChannelPermissions(
                allow_file_read=True,
                allow_file_write=False,
                allow_file_delete=False,
                allow_command_execution=False,
                allow_browser_access=False,
                allow_network_access=True,
                allow_subagent_spawn=False,
            ),
            require_approval_for_destructive=True,
            require_approval_for_sensitive=True,
        )
        
        # Authenticated channel (moderate restrictions)
        self.channels["default_authenticated"] = ChannelSecurityMetadata(
            channel_id="default_authenticated",
            channel_type="authenticated",
            auth_level="authenticated",
            permissions=ChannelPermissions(
                allow_file_read=True,
                allow_file_write=True,
                allow_file_delete=False,
                allow_command_execution=True,
                allow_browser_access=True,
                allow_network_access=True,
                allow_subagent_spawn=True,
            ),
            require_approval_for_destructive=True,
            require_approval_for_sensitive=True,
        )
        
        # Admin channel (least restrictive)
        self.channels["default_admin"] = ChannelSecurityMetadata(
            channel_id="default_admin",
            channel_type="admin",
            auth_level="admin",
            permissions=ChannelPermissions(
                allow_file_read=True,
                allow_file_write=True,
                allow_file_delete=True,
                allow_command_execution=True,
                allow_browser_access=True,
                allow_network_access=True,
                allow_subagent_spawn=True,
            ),
            require_approval_for_destructive=False,
            require_approval_for_sensitive=False,
        )
    
    def get_metadata(self, channel_id: str) -> ChannelSecurityMetadata:
        """
        Get security metadata for channel
        
        Args:
            channel_id: Channel ID
            
        Returns:
            Channel security metadata
        """
        if channel_id in self.channels:
            return self.channels[channel_id]
        
        # Return default authenticated profile
        logger.info(f"No security metadata for {channel_id}, using default_authenticated")
        return self.channels["default_authenticated"]
    
    def set_metadata(self, metadata: ChannelSecurityMetadata) -> None:
        """
        Set security metadata for channel
        
        Args:
            metadata: Channel security metadata
        """
        self.channels[metadata.channel_id] = metadata
        logger.info(f"Updated security metadata for channel: {metadata.channel_id}")
    
    def check_permission(
        self,
        channel_id: str,
        permission: str
    ) -> bool:
        """
        Check if channel has permission
        
        Args:
            channel_id: Channel ID
            permission: Permission name (e.g., "allow_file_write")
            
        Returns:
            True if allowed
        """
        metadata = self.get_metadata(channel_id)
        return getattr(metadata.permissions, permission, False)
    
    def check_tool_allowed(
        self,
        channel_id: str,
        tool_name: str
    ) -> bool:
        """
        Check if tool is allowed for channel
        
        Args:
            channel_id: Channel ID
            tool_name: Tool name
            
        Returns:
            True if allowed
        """
        metadata = self.get_metadata(channel_id)
        return metadata.permissions.is_tool_allowed(tool_name)


# Global security manager instance
_security_manager: ChannelSecurityManager | None = None


def get_security_manager() -> ChannelSecurityManager:
    """
    Get global channel security manager
    
    Returns:
        Global security manager
    """
    global _security_manager
    
    if _security_manager is None:
        _security_manager = ChannelSecurityManager()
    
    return _security_manager
