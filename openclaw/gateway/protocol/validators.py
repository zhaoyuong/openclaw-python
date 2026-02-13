"""
Request parameter validation

Provides Pydantic models for validating Gateway method parameters,
matching the TypeScript schema validation with Ajv.
"""

from typing import Optional, List, Any
from pydantic import BaseModel, Field, field_validator


# ============================================================================
# Agent Methods
# ============================================================================

class AgentParams(BaseModel):
    """Parameters for agent method"""
    message: str = Field(..., description="Message to send to agent")
    sessionKey: Optional[str] = Field(None, description="Session key")
    thinkingLevel: Optional[str] = Field(None, description="Thinking level")
    model: Optional[str] = Field(None, description="Model to use")
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    maxTokens: Optional[int] = Field(None, gt=0)
    files: Optional[List[dict]] = Field(None, description="Attached files")
    
    @field_validator("thinkingLevel")
    @classmethod
    def validate_thinking_level(cls, v):
        if v and v not in ["off", "quick", "medium", "deep", "full"]:
            raise ValueError("Invalid thinking level")
        return v


# ============================================================================
# Chat Methods
# ============================================================================

class ChatSendParams(BaseModel):
    """Parameters for chat.send"""
    message: str
    sessionKey: Optional[str] = None
    model: Optional[str] = None
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    stream: Optional[bool] = False


class ChatAbortParams(BaseModel):
    """Parameters for chat.abort"""
    runId: Optional[str] = None
    sessionKey: Optional[str] = None


class ChatHistoryParams(BaseModel):
    """Parameters for chat.history"""
    sessionKey: Optional[str] = None
    limit: Optional[int] = Field(None, gt=0, le=1000)
    offset: Optional[int] = Field(None, ge=0)


# ============================================================================
# Session Methods
# ============================================================================

class SessionsListParams(BaseModel):
    """Parameters for sessions.list"""
    agentId: Optional[str] = None
    spawnedBy: Optional[str] = None
    label: Optional[str] = None
    search: Optional[str] = None
    activeMinutes: Optional[int] = Field(None, gt=0)
    offset: Optional[int] = Field(None, ge=0)
    limit: Optional[int] = Field(None, gt=0, le=1000)
    sortBy: Optional[str] = None
    sortOrder: Optional[str] = None
    
    @field_validator("sortOrder")
    @classmethod
    def validate_sort_order(cls, v):
        if v and v not in ["asc", "desc"]:
            raise ValueError("sortOrder must be 'asc' or 'desc'")
        return v


class SessionsPreviewParams(BaseModel):
    """Parameters for sessions.preview"""
    key: Optional[str] = None
    sessionId: Optional[str] = None
    label: Optional[str] = None
    limit: Optional[int] = Field(10, gt=0, le=100)


class SessionsResolveParams(BaseModel):
    """Parameters for sessions.resolve"""
    key: Optional[str] = None
    sessionId: Optional[str] = None
    label: Optional[str] = None


class SessionsPatchParams(BaseModel):
    """Parameters for sessions.patch"""
    key: Optional[str] = None
    sessionId: Optional[str] = None
    label: Optional[str] = None
    patch: dict = Field(..., description="Patch data")


class SessionsResetParams(BaseModel):
    """Parameters for sessions.reset"""
    key: Optional[str] = None
    sessionId: Optional[str] = None
    label: Optional[str] = None


class SessionsDeleteParams(BaseModel):
    """Parameters for sessions.delete"""
    key: Optional[str] = None
    sessionId: Optional[str] = None
    label: Optional[str] = None


class SessionsCompactParams(BaseModel):
    """Parameters for sessions.compact"""
    key: Optional[str] = None
    sessionId: Optional[str] = None
    label: Optional[str] = None


# ============================================================================
# Config Methods
# ============================================================================

class ConfigSetParams(BaseModel):
    """Parameters for config.set"""
    config: dict = Field(..., description="New configuration")


class ConfigPatchParams(BaseModel):
    """Parameters for config.patch"""
    patch: dict = Field(..., description="Configuration patch")


# ============================================================================
# Agents Methods
# ============================================================================

class AgentsFilesListParams(BaseModel):
    """Parameters for agents.files.list"""
    agentId: Optional[str] = "main"


class AgentsFilesGetParams(BaseModel):
    """Parameters for agents.files.get"""
    agentId: Optional[str] = "main"
    filename: str


class AgentsFilesSetParams(BaseModel):
    """Parameters for agents.files.set"""
    agentId: Optional[str] = "main"
    filename: str
    content: str


# ============================================================================
# Channel Methods
# ============================================================================

class ChannelsLogoutParams(BaseModel):
    """Parameters for channels.logout"""
    channelId: str


# ============================================================================
# Cron Methods
# ============================================================================

class CronAddParams(BaseModel):
    """Parameters for cron.add"""
    job: dict = Field(..., description="Job configuration")
    
    @field_validator("job")
    @classmethod
    def validate_job(cls, v):
        required_fields = ["id", "schedule", "action"]
        for field in required_fields:
            if field not in v:
                raise ValueError(f"Job missing required field: {field}")
        return v


class CronRemoveParams(BaseModel):
    """Parameters for cron.remove"""
    jobId: str


class CronStatusParams(BaseModel):
    """Parameters for cron.status"""
    jobId: str


# ============================================================================
# Node Methods
# ============================================================================

class NodeInvokeParams(BaseModel):
    """Parameters for node.invoke"""
    nodeId: str
    command: str
    params: Optional[dict] = None


class NodePairApproveParams(BaseModel):
    """Parameters for node.pair.approve"""
    nodeId: str


class NodePairRejectParams(BaseModel):
    """Parameters for node.pair.reject"""
    nodeId: str
    reason: Optional[str] = None


# ============================================================================
# Device Methods
# ============================================================================

class DevicePairApproveParams(BaseModel):
    """Parameters for device.pair.approve"""
    deviceId: str


class DevicePairRejectParams(BaseModel):
    """Parameters for device.pair.reject"""
    deviceId: str
    reason: Optional[str] = None


# ============================================================================
# Validator Registry
# ============================================================================

# Map method names to their parameter validators
PARAM_VALIDATORS = {
    # Agent
    "agent": AgentParams,
    
    # Chat
    "chat.send": ChatSendParams,
    "chat.abort": ChatAbortParams,
    "chat.history": ChatHistoryParams,
    
    # Sessions
    "sessions.list": SessionsListParams,
    "sessions.preview": SessionsPreviewParams,
    "sessions.resolve": SessionsResolveParams,
    "sessions.patch": SessionsPatchParams,
    "sessions.reset": SessionsResetParams,
    "sessions.delete": SessionsDeleteParams,
    "sessions.compact": SessionsCompactParams,
    
    # Config
    "config.set": ConfigSetParams,
    "config.patch": ConfigPatchParams,
    
    # Agents
    "agents.files.list": AgentsFilesListParams,
    "agents.files.get": AgentsFilesGetParams,
    "agents.files.set": AgentsFilesSetParams,
    
    # Channels
    "channels.logout": ChannelsLogoutParams,
    
    # Cron
    "cron.add": CronAddParams,
    "cron.remove": CronRemoveParams,
    "cron.status": CronStatusParams,
    
    # Nodes
    "node.invoke": NodeInvokeParams,
    "node.pair.approve": NodePairApproveParams,
    "node.pair.reject": NodePairRejectParams,
    
    # Devices
    "device.pair.approve": DevicePairApproveParams,
    "device.pair.reject": DevicePairRejectParams,
}


def validate_method_params(method: str, params: dict) -> Any:
    """
    Validate method parameters
    
    Args:
        method: Method name
        params: Parameters dictionary
        
    Returns:
        Validated params as Pydantic model
        
    Raises:
        ValidationError: If params are invalid
    """
    validator = PARAM_VALIDATORS.get(method)
    if validator:
        return validator(**params)
    return params  # No validation for unknown methods
