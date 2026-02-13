"""
Session entry patching with field validation

This module implements session entry patch logic matching the TypeScript implementation.
Supports updating session fields with validation and constraints.
"""

import logging
import time
import uuid
from typing import Any, Dict, Optional

from openclaw.agents.session_entry import SessionEntry, merge_session_entry

logger = logging.getLogger(__name__)


# ============================================================================
# Field Validation
# ============================================================================

def validate_thinking_level(value: Any) -> Optional[str]:
    """
    Validate thinking level
    
    Args:
        value: Thinking level value
        
    Returns:
        Normalized thinking level or None
        
    Raises:
        ValueError: If invalid
    """
    if value is None:
        return None
    
    valid_levels = ["low", "medium", "high", "xhigh"]
    value_str = str(value).lower()
    
    if value_str not in valid_levels:
        raise ValueError(f"Invalid thinking level: {value}. Must be one of: {valid_levels}")
    
    return value_str


def validate_verbose_level(value: Any) -> Optional[str]:
    """Validate verbose level"""
    if value is None:
        return None
    return str(value)


def validate_reasoning_level(value: Any) -> Optional[str]:
    """Validate reasoning level"""
    if value is None:
        return None
    return str(value)


def validate_elevated_level(value: Any) -> Optional[str]:
    """Validate elevated level"""
    if value is None:
        return None
    return str(value)


def validate_response_usage(value: Any) -> Optional[str]:
    """Validate response usage mode"""
    if value is None:
        return None
    
    valid_modes = ["on", "off", "tokens", "full"]
    value_str = str(value)
    
    if value_str not in valid_modes:
        raise ValueError(f"Invalid response usage: {value}. Must be one of: {valid_modes}")
    
    return value_str


def validate_send_policy(value: Any) -> Optional[str]:
    """Validate send policy"""
    if value is None:
        return None
    
    valid_policies = ["allow", "deny"]
    value_str = str(value)
    
    if value_str not in valid_policies:
        raise ValueError(f"Invalid send policy: {value}. Must be one of: {valid_policies}")
    
    return value_str


def validate_group_activation(value: Any) -> Optional[str]:
    """Validate group activation mode"""
    if value is None:
        return None
    
    valid_modes = ["mention", "always"]
    value_str = str(value)
    
    if value_str not in valid_modes:
        raise ValueError(f"Invalid group activation: {value}. Must be one of: {valid_modes}")
    
    return value_str


def validate_label(value: Any) -> Optional[str]:
    """Validate session label"""
    if value is None:
        return None
    
    label = str(value).strip()
    
    if len(label) == 0:
        return None
    
    if len(label) > 64:
        raise ValueError(f"Label must be 64 characters or less, got {len(label)}")
    
    return label


def validate_spawned_by(value: Any, existing_value: Optional[str]) -> Optional[str]:
    """
    Validate spawned_by (immutable once set)
    
    Args:
        value: New value
        existing_value: Current value
        
    Returns:
        Validated value
        
    Raises:
        ValueError: If attempting to change existing value
    """
    if value is None:
        return existing_value
    
    new_value = str(value).strip()
    
    if existing_value is not None and existing_value != new_value:
        raise ValueError("Cannot change spawned_by once set")
    
    return new_value


# ============================================================================
# Label Uniqueness Check
# ============================================================================

def check_label_uniqueness(
    label: Optional[str],
    store: Dict[str, SessionEntry],
    current_key: str
) -> None:
    """
    Check if label is unique within store
    
    Args:
        label: Label to check
        store: Session store
        current_key: Current session key (excluded from check)
        
    Raises:
        ValueError: If label is not unique
    """
    if not label:
        return
    
    for key, entry in store.items():
        if key == current_key:
            continue
        
        if entry.label == label:
            raise ValueError(f"Label '{label}' is already used by session: {key}")


# ============================================================================
# Session Patch Application
# ============================================================================

def apply_sessions_patch_to_store(
    store: Dict[str, SessionEntry],
    store_key: str,
    patch: Dict[str, Any],
    model_catalog: Optional[Any] = None
) -> SessionEntry:
    """
    Apply patch to session entry with validation
    
    Args:
        store: Session store dictionary
        store_key: Key of session to patch
        patch: Patch data
        model_catalog: Optional model catalog for validation
        
    Returns:
        Updated SessionEntry
        
    Raises:
        ValueError: If validation fails
    """
    # Get existing entry or create new
    existing = store.get(store_key)
    
    # Build validated patch
    validated_patch: Dict[str, Any] = {}
    
    # =========================================================================
    # Core fields
    # =========================================================================
    
    # Session ID (generate if new)
    if "session_id" in patch:
        validated_patch["session_id"] = str(patch["session_id"])
    elif not existing:
        validated_patch["session_id"] = str(uuid.uuid4())
    
    # Updated timestamp
    now_ms = int(time.time() * 1000)
    validated_patch["updated_at"] = max(
        existing.updated_at if existing else 0,
        patch.get("updated_at", 0),
        now_ms
    )
    
    # =========================================================================
    # Immutable fields
    # =========================================================================
    
    if "spawned_by" in patch:
        validated_patch["spawned_by"] = validate_spawned_by(
            patch["spawned_by"],
            existing.spawned_by if existing else None
        )
    
    # =========================================================================
    # Label (with uniqueness check)
    # =========================================================================
    
    if "label" in patch:
        label = validate_label(patch["label"])
        if label:
            check_label_uniqueness(label, store, store_key)
        validated_patch["label"] = label
    
    # =========================================================================
    # Model configuration
    # =========================================================================
    
    if "thinking_level" in patch:
        validated_patch["thinking_level"] = validate_thinking_level(patch["thinking_level"])
    
    if "verbose_level" in patch:
        validated_patch["verbose_level"] = validate_verbose_level(patch["verbose_level"])
    
    if "reasoning_level" in patch:
        validated_patch["reasoning_level"] = validate_reasoning_level(patch["reasoning_level"])
    
    if "elevated_level" in patch:
        validated_patch["elevated_level"] = validate_elevated_level(patch["elevated_level"])
    
    if "provider_override" in patch:
        validated_patch["provider_override"] = patch["provider_override"]
    
    if "model_override" in patch:
        validated_patch["model_override"] = patch["model_override"]
    
    # =========================================================================
    # Execution environment
    # =========================================================================
    
    if "exec_host" in patch:
        validated_patch["exec_host"] = patch["exec_host"]
    
    if "exec_security" in patch:
        validated_patch["exec_security"] = patch["exec_security"]
    
    if "exec_ask" in patch:
        validated_patch["exec_ask"] = patch["exec_ask"]
    
    if "exec_node" in patch:
        validated_patch["exec_node"] = patch["exec_node"]
    
    # =========================================================================
    # Behavior configuration
    # =========================================================================
    
    if "response_usage" in patch:
        validated_patch["response_usage"] = validate_response_usage(patch["response_usage"])
    
    if "send_policy" in patch:
        validated_patch["send_policy"] = validate_send_policy(patch["send_policy"])
    
    if "group_activation" in patch:
        validated_patch["group_activation"] = validate_group_activation(patch["group_activation"])
    
    # =========================================================================
    # Display and metadata
    # =========================================================================
    
    if "display_name" in patch:
        validated_patch["display_name"] = patch["display_name"]
    
    if "subject" in patch:
        validated_patch["subject"] = patch["subject"]
    
    # =========================================================================
    # Token tracking (allow updates)
    # =========================================================================
    
    if "input_tokens" in patch:
        validated_patch["input_tokens"] = patch["input_tokens"]
    
    if "output_tokens" in patch:
        validated_patch["output_tokens"] = patch["output_tokens"]
    
    if "total_tokens" in patch:
        validated_patch["total_tokens"] = patch["total_tokens"]
    
    # =========================================================================
    # Other fields (pass through)
    # =========================================================================
    
    passthrough_fields = [
        "session_file", "system_sent", "aborted_last_run",
        "chat_type", "channel", "group_id", "group_channel", "space",
        "tts_auto", "auth_profile_override", "auth_profile_override_source",
        "queue_mode", "queue_debounce_ms", "queue_cap", "queue_drop",
        "model_provider", "model", "context_tokens",
        "compaction_count", "memory_flush_at", "memory_flush_compaction_count",
        "origin", "delivery_context",
        "last_channel", "last_to", "last_account_id", "last_thread_id",
        "last_heartbeat_text", "last_heartbeat_sent_at",
        "skills_snapshot", "system_prompt_report",
    ]
    
    for field in passthrough_fields:
        if field in patch:
            validated_patch[field] = patch[field]
    
    # =========================================================================
    # Merge and update store
    # =========================================================================
    
    updated_entry = merge_session_entry(existing, validated_patch)
    store[store_key] = updated_entry
    
    logger.info(f"Patched session: {store_key}")
    
    return updated_entry
