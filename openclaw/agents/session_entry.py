"""
Session entry models matching TypeScript SessionEntry structure

This module provides complete session metadata models that align with
openclaw TypeScript implementation.
"""
from __future__ import annotations


from typing import Any, Literal, Optional
from pydantic import BaseModel, Field


class SessionOrigin(BaseModel):
    """Session origin metadata - where the session originated from"""
    
    label: Optional[str] = None
    provider: Optional[str] = None
    surface: Optional[str] = None
    chat_type: Optional[str] = None
    from_: Optional[str] = Field(None, alias="from")
    to: Optional[str] = None
    account_id: Optional[str] = None
    thread_id: Optional[str | int] = None

    class Config:
        populate_by_name = True


class DeliveryContext(BaseModel):
    """Message delivery context - where to send responses"""
    
    channel: Optional[str] = None
    to: Optional[str] = None
    account_id: Optional[str] = None
    thread_id: Optional[str | int] = None


class SessionEntry(BaseModel):
    """
    Complete session metadata matching TypeScript SessionEntry
    
    This represents the session metadata stored in sessions.json.
    The actual conversation messages are stored separately in .jsonl transcript files.
    """
    
    # =========================================================================
    # Core fields
    # =========================================================================
    
    session_id: str
    """Unique session identifier (UUID v4)"""
    
    updated_at: int
    """Last update timestamp in milliseconds since epoch"""
    
    session_file: Optional[str] = None
    """Relative path to transcript file (e.g., "{sessionId}.jsonl")"""
    
    spawned_by: Optional[str] = None
    """Parent session key that spawned this session (for subagent sessions)"""
    
    # =========================================================================
    # State flags
    # =========================================================================
    
    system_sent: Optional[bool] = None
    """Whether system message was sent"""
    
    aborted_last_run: Optional[bool] = None
    """Whether the last run was aborted"""
    
    # =========================================================================
    # Chat type and channel information
    # =========================================================================
    
    chat_type: Optional[str] = None
    """Type of chat (dm, group, channel, etc.)"""
    
    channel: Optional[str] = None
    """Channel name (telegram, discord, slack, etc.)"""
    
    group_id: Optional[str] = None
    """Group identifier"""
    
    subject: Optional[str] = None
    """Subject or title"""
    
    group_channel: Optional[str] = None
    """Group channel identifier"""
    
    space: Optional[str] = None
    """Workspace or space identifier"""
    
    # =========================================================================
    # Model configuration
    # =========================================================================
    
    thinking_level: Optional[str] = None
    """Thinking level (low, medium, high, xhigh)"""
    
    verbose_level: Optional[str] = None
    """Verbose level"""
    
    reasoning_level: Optional[str] = None
    """Reasoning level"""
    
    elevated_level: Optional[str] = None
    """Elevated level"""
    
    tts_auto: Optional[str] = None
    """Text-to-speech auto mode"""
    
    provider_override: Optional[str] = None
    """Provider override (anthropic, openai, etc.)"""
    
    model_override: Optional[str] = None
    """Model override (claude-3-5-sonnet, gpt-4, etc.)"""
    
    auth_profile_override: Optional[str] = None
    """Auth profile override"""
    
    auth_profile_override_source: Optional[Literal["auto", "user"]] = None
    """Source of auth profile override"""
    
    auth_profile_override_compaction_count: Optional[int] = None
    """Compaction count when auth profile was overridden"""
    
    # =========================================================================
    # Execution environment
    # =========================================================================
    
    exec_host: Optional[str] = None
    """Execution host"""
    
    exec_security: Optional[str] = None
    """Execution security level"""
    
    exec_ask: Optional[str] = None
    """Execution ask mode"""
    
    exec_node: Optional[str] = None
    """Execution node"""
    
    # =========================================================================
    # Behavior configuration
    # =========================================================================
    
    response_usage: Optional[Literal["on", "off", "tokens", "full"]] = None
    """Response usage display mode"""
    
    send_policy: Optional[Literal["allow", "deny"]] = None
    """Send policy for outbound messages"""
    
    group_activation: Optional[Literal["mention", "always"]] = None
    """Group activation mode"""
    
    group_activation_needs_system_intro: Optional[bool] = None
    """Whether group activation needs system intro"""
    
    queue_mode: Optional[str] = None
    """Queue mode (steer, followup, collect, queue, interrupt, etc.)"""
    
    queue_debounce_ms: Optional[int] = None
    """Queue debounce milliseconds"""
    
    queue_cap: Optional[int] = None
    """Queue capacity limit"""
    
    queue_drop: Optional[Literal["old", "new", "summarize"]] = None
    """Queue drop strategy when capacity is exceeded"""
    
    # =========================================================================
    # Token tracking
    # =========================================================================
    
    input_tokens: Optional[int] = None
    """Total input tokens consumed"""
    
    output_tokens: Optional[int] = None
    """Total output tokens generated"""
    
    total_tokens: Optional[int] = None
    """Total tokens (input + output)"""
    
    model_provider: Optional[str] = None
    """Current model provider"""
    
    model: Optional[str] = None
    """Current model"""
    
    context_tokens: Optional[int] = None
    """Context window size in tokens"""
    
    # =========================================================================
    # Compaction and memory management
    # =========================================================================
    
    compaction_count: Optional[int] = None
    """Number of times transcript has been compacted"""
    
    memory_flush_at: Optional[int] = None
    """Timestamp when memory should be flushed"""
    
    memory_flush_compaction_count: Optional[int] = None
    """Compaction count at last memory flush"""
    
    # =========================================================================
    # CLI sessions
    # =========================================================================
    
    cli_session_ids: Optional[dict[str, str]] = None
    """CLI session IDs mapping"""
    
    claude_cli_session_id: Optional[str] = None
    """Claude CLI session ID"""
    
    # =========================================================================
    # Labels and display
    # =========================================================================
    
    label: Optional[str] = None
    """User-defined label (max 64 chars, unique per store)"""
    
    display_name: Optional[str] = None
    """Display name for UI"""
    
    # =========================================================================
    # Origin and delivery
    # =========================================================================
    
    origin: Optional[SessionOrigin] = None
    """Session origin metadata"""
    
    delivery_context: Optional[DeliveryContext] = None
    """Message delivery context"""
    
    last_channel: Optional[str] = None
    """Last channel used"""
    
    last_to: Optional[str] = None
    """Last recipient"""
    
    last_account_id: Optional[str] = None
    """Last account ID"""
    
    last_thread_id: Optional[str | int] = None
    """Last thread ID"""
    
    # =========================================================================
    # Heartbeat
    # =========================================================================
    
    last_heartbeat_text: Optional[str] = None
    """Last delivered heartbeat payload"""
    
    last_heartbeat_sent_at: Optional[int] = None
    """Timestamp (ms) when lastHeartbeatText was delivered"""
    
    # =========================================================================
    # Skills and system prompt snapshots
    # =========================================================================
    
    skills_snapshot: Optional[dict[str, Any]] = None
    """Skills snapshot for this session"""
    
    system_prompt_report: Optional[dict[str, Any]] = None
    """System prompt report"""

    class Config:
        populate_by_name = True


def merge_session_entry(
    existing: Optional[SessionEntry],
    patch: dict[str, Any],
) -> SessionEntry:
    """
    Merge a patch into an existing session entry
    
    Args:
        existing: Existing session entry (if any)
        patch: Partial session entry to merge
        
    Returns:
        Merged session entry
    """
    import uuid
    import time
    
    # Generate session_id if not provided
    session_id = patch.get("session_id") or (existing.session_id if existing else str(uuid.uuid4()))
    
    # Use max of existing, patch, and current time for updated_at
    now_ms = int(time.time() * 1000)
    updated_at = max(
        existing.updated_at if existing else 0,
        patch.get("updated_at", 0),
        now_ms
    )
    
    if not existing:
        # Create new entry from patch
        return SessionEntry(
            session_id=session_id,
            updated_at=updated_at,
            **{k: v for k, v in patch.items() if k not in ["session_id", "updated_at"]}
        )
    
    # Merge existing with patch
    existing_dict = existing.model_dump(exclude_unset=False)
    existing_dict.update(patch)
    existing_dict["session_id"] = session_id
    existing_dict["updated_at"] = updated_at
    
    return SessionEntry(**existing_dict)
