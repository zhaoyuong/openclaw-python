"""
Method authorization with roles and scopes

Implements role-based access control matching the TypeScript implementation.
"""

import logging
from typing import Set, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


# ============================================================================
# Roles and Scopes
# ============================================================================

class Role:
    """Authorization roles"""
    OPERATOR = "operator"
    NODE = "node"


class Scope:
    """Authorization scopes for operator role"""
    ADMIN = "operator.admin"
    READ = "operator.read"
    WRITE = "operator.write"
    APPROVALS = "operator.approvals"
    PAIRING = "operator.pairing"


@dataclass
class AuthContext:
    """Authentication context for a connection"""
    role: str = Role.OPERATOR
    scopes: Set[str] = None
    user: Optional[str] = None
    device_id: Optional[str] = None
    node_id: Optional[str] = None
    
    def __post_init__(self):
        if self.scopes is None:
            self.scopes = set()


# ============================================================================
# Method Authorization Requirements
# ============================================================================

# Methods that require specific roles or scopes
METHOD_REQUIREMENTS = {
    # Admin methods
    "config.set": [Scope.ADMIN],
    "config.patch": [Scope.ADMIN],
    "config.apply": [Scope.ADMIN],
    "wizard.start": [Scope.ADMIN],
    "wizard.next": [Scope.ADMIN],
    "wizard.cancel": [Scope.ADMIN],
    "update.run": [Scope.ADMIN],
    
    # Exec approvals (admin or approvals scope)
    "exec.approvals.get": [Scope.ADMIN, Scope.APPROVALS],
    "exec.approvals.set": [Scope.ADMIN, Scope.APPROVALS],
    "exec.approvals.node.get": [Scope.ADMIN, Scope.APPROVALS],
    "exec.approvals.node.set": [Scope.ADMIN, Scope.APPROVALS],
    
    # Node pairing (admin or pairing scope)
    "node.pair.approve": [Scope.ADMIN, Scope.PAIRING],
    "node.pair.reject": [Scope.ADMIN, Scope.PAIRING],
    
    # Device pairing (admin or pairing scope)
    "device.pair.approve": [Scope.ADMIN, Scope.PAIRING],
    "device.pair.reject": [Scope.ADMIN, Scope.PAIRING],
    "device.token.rotate": [Scope.ADMIN, Scope.PAIRING],
    "device.token.revoke": [Scope.ADMIN, Scope.PAIRING],
    
    # Node-only methods
    "node.invoke": [Role.NODE],
    "node.invoke.result": [Role.NODE],
    "node.event": [Role.NODE],
    "skills.bins": [Role.NODE],
}


# Public methods (no authorization required)
PUBLIC_METHODS = {
    "connect",
    "health",
    "status",
    "ping",
}


# Read-only methods (read scope sufficient)
READ_ONLY_METHODS = {
    "config.get",
    "sessions.list",
    "sessions.preview",
    "sessions.resolve",
    "agents.list",
    "agents.files.list",
    "agents.files.get",
    "channels.list",
    "channels.status",
    "models.list",
    "cron.list",
    "cron.status",
    "node.list",
    "device.pair.list",
    "logs.tail",
}


def authorize_gateway_method(method: str, auth_context: AuthContext) -> bool:
    """
    Authorize method call based on role and scopes
    
    Args:
        method: Method name
        auth_context: Authentication context
        
    Returns:
        True if authorized, False otherwise
    """
    # Public methods always allowed
    if method in PUBLIC_METHODS:
        return True
    
    # Check read-only methods
    if method in READ_ONLY_METHODS:
        # Read scope or admin scope
        if Scope.READ in auth_context.scopes or Scope.ADMIN in auth_context.scopes:
            return True
        # Default: allow for operator role
        if auth_context.role == Role.OPERATOR:
            return True
    
    # Check specific requirements
    requirements = METHOD_REQUIREMENTS.get(method)
    if requirements:
        for requirement in requirements:
            # Check role match
            if requirement == auth_context.role:
                return True
            
            # Check scope match
            if requirement in auth_context.scopes:
                return True
        
        # No match found
        logger.warning(
            f"Authorization denied for {method}: "
            f"role={auth_context.role}, scopes={auth_context.scopes}, "
            f"required={requirements}"
        )
        return False
    
    # Default: allow for operator role
    if auth_context.role == Role.OPERATOR:
        return True
    
    # Node role: deny unknown methods
    if auth_context.role == Role.NODE:
        logger.warning(f"Node attempted unauthorized method: {method}")
        return False
    
    # Default: allow
    return True
