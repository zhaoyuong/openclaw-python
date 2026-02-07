"""
Session management for agent conversations
"""

import json
import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from openclaw.agents.session_ids import generate_session_id, looks_like_session_id
from openclaw.routing.session_key import (
    build_agent_main_session_key,
    build_agent_peer_session_key,
    normalize_agent_id,
    parse_agent_session_key,
)

logger = logging.getLogger(__name__)


class Message(BaseModel):
    """A single message in a conversation"""

    role: str  # "user", "assistant", "system", "tool"
    content: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    tool_calls: list[dict[str, Any]] | None = None
    tool_call_id: str | None = None
    name: str | None = None  # For tool results
    images: list[str] | None = None  # Image URLs or paths

    def to_api_format(self) -> dict[str, Any]:
        """Convert to API format for LLM calls"""
        # If there are no images, keep the content as a simple string
        # For compatibility with LLMs that don't support multimodal input
        if not self.images:
            msg = {"role": self.role, "content": self.content}
        else:
            # Bulid Multimodal content array, with text and images as separate entries
            content_array = [{"type": "text", "text": self.content}]
            for img in self.images:
                content_array.append(
                    {
                        "type": "image_url",
                        "image_url": {"url": img},  # URL could be real url or base64
                    }
                )
            msg = {"role": self.role, "content": content_array}

        if self.tool_calls:
            msg["tool_calls"] = self.tool_calls

        if self.tool_call_id:
            msg["tool_call_id"] = self.tool_call_id

        if self.name:
            msg["name"] = self.name

        return msg


class Session(BaseModel):
    """
    Manages a conversation session with persistence
    """

    session_id: str
    workspace_dir: Path
    messages: list[Message] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())

    model_config = {"arbitrary_types_allowed": True}

    def __init__(self, session_id: str, workspace_dir: Path, **kwargs):
        """Initialize session, loading from disk if exists"""
        super().__init__(session_id=session_id, workspace_dir=workspace_dir, **kwargs)

        # Create sessions directory
        self._sessions_dir.mkdir(parents=True, exist_ok=True)

        # Load existing session if exists
        if self._session_file.exists() and not self.messages:
            self._load()

    @property
    def _sessions_dir(self) -> Path:
        """Get sessions directory"""
        return self.workspace_dir / ".sessions"

    @property
    def _session_file(self) -> Path:
        """Get session file path"""
        return self._sessions_dir / f"{self.session_id}.json"

    def add_message(self, role: str, content: str, **kwargs) -> Message:
        """Add a message to the session"""
        msg = Message(role=role, content=content, **kwargs)
        self.messages.append(msg)
        self.updated_at = datetime.now(UTC).isoformat()
        self._save()
        return msg

    def add_user_message(self, content: str, images: list[str] | None = None) -> Message:
        """Add a user message(support optional images)"""
        return self.add_message("user", content, images=images)

    def add_assistant_message(
        self, content: str, tool_calls: list[dict[str, Any]] | None = None
    ) -> Message:
        """Add an assistant message"""
        return self.add_message("assistant", content, tool_calls=tool_calls)

    def add_system_message(self, content: str) -> Message:
        """Add a system message"""
        return self.add_message("system", content)

    def add_tool_message(self, tool_call_id: str, content: str, name: str | None = None) -> Message:
        """Add a tool result message"""
        return self.add_message("tool", content, tool_call_id=tool_call_id, name=name)

    def get_messages(self, limit: int | None = None) -> list[Message]:
        """Get messages, optionally limited to last N"""
        if limit is None:
            return self.messages
        return self.messages[-limit:]

    def get_messages_for_api(self, limit: int | None = None) -> list[dict[str, Any]]:
        """Get messages in API format"""
        messages = self.get_messages(limit)
        return [msg.to_api_format() for msg in messages]

    def clear(self) -> None:
        """Clear all messages"""
        self.messages = []
        self.updated_at = datetime.utcnow().isoformat()
        self._save()

    def set_metadata(self, key: str, value: Any) -> None:
        """Set metadata value"""
        self.metadata[key] = value
        self._save()

    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Get metadata value"""
        return self.metadata.get(key, default)

    def _save(self) -> None:
        """Save session to disk"""
        try:
            data = {
                "session_id": self.session_id,
                "messages": [msg.model_dump() for msg in self.messages],
                "metadata": self.metadata,
                "created_at": self.created_at,
                "updated_at": self.updated_at,
            }
            with open(self._session_file, "w") as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save session: {e}")

    def _load(self) -> None:
        """Load session from disk"""
        try:
            with open(self._session_file) as f:
                data = json.load(f)

            self.messages = [Message(**msg) for msg in data.get("messages", [])]
            self.metadata = data.get("metadata", {})
            self.created_at = data.get("created_at", self.created_at)
            self.updated_at = data.get("updated_at", self.updated_at)
        except Exception as e:
            logger.error(f"Failed to load session: {e}")

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary"""
        return {
            "sessionId": self.session_id,
            "messageCount": len(self.messages),
            "messages": [msg.model_dump() for msg in self.messages],
            "metadata": self.metadata,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
        }


class SessionManager:
    """
    Manages multiple sessions with enhanced session key support

    New features:
    - Session key format (agent:id:channel:group:id)
    - UUID v4 session IDs with validation
    - DM scope modes (main, per-peer, per-channel-peer, per-account-channel-peer)
    - Agent ID normalization
    - Session key to session ID mapping
    """

    def __init__(self, workspace_dir: Path, agent_id: str = "main"):
        """
        Initialize session manager

        Args:
            workspace_dir: Base directory for session storage
            agent_id: Agent identifier (default: "main")
        """
        self.workspace_dir = Path(workspace_dir)
        self.agent_id = normalize_agent_id(agent_id)
        self._sessions: dict[str, Session] = {}

        # Create workspace directory
        self.workspace_dir.mkdir(parents=True, exist_ok=True)

        # Session key to session ID mapping
        sessions_dir = self.workspace_dir / ".sessions"
        sessions_dir.mkdir(parents=True, exist_ok=True)
        self._session_map_file = sessions_dir / "session_map.json"
        self._session_map: dict[str, str] = self._load_session_map()

    def _load_session_map(self) -> dict[str, str]:
        """Load session key -> session ID mapping."""
        if self._session_map_file.exists():
            try:
                with open(self._session_map_file) as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load session map: {e}")
        return {}

    def _save_session_map(self):
        """Save session key -> session ID mapping."""
        try:
            with open(self._session_map_file, "w") as f:
                json.dump(self._session_map, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save session map: {e}")

    def generate_session_id(self) -> str:
        """Generate a new UUID v4 session ID."""
        return generate_session_id()

    def validate_session_id(self, session_id: str) -> bool:
        """Validate session ID format (UUID v4)."""
        return looks_like_session_id(session_id)

    def get_or_create_session(
        self,
        session_id: str | None = None,
        session_key: str | None = None,
        channel: str | None = None,
        peer_kind: str | None = None,
        peer_id: str | None = None,
        dm_scope: str = "main",
    ) -> Session:
        """
        Get existing session or create new one with session key support.

        Args:
            session_id: Direct session ID (legacy, optional)
            session_key: Session key (agent:id:..., optional)
            channel: Channel name (telegram, discord, etc.)
            peer_kind: Peer type (dm, group, channel)
            peer_id: Peer identifier
            dm_scope: DM scope mode (main, per-peer, per-channel-peer, per-account-channel-peer)

        Returns:
            Session instance
        """
        # Build session key if not provided
        if session_key is None and channel and peer_kind and peer_id:
            # Build peer session key. Historically 'per-peer' omits channel,
            # but some integration expectations prefer the channel to be present
            # when a channel is provided. Use per-channel-peer form when a
            # channel is present to make session keys more explicit.
            if peer_kind == "dm" and dm_scope == "per-peer" and channel:
                normalized_channel = channel.strip().lower()
                session_key = f"agent:{self.agent_id}:{normalized_channel}:dm:{peer_id}"
            else:
                session_key = build_agent_peer_session_key(
                    self.agent_id, channel, peer_kind, peer_id, dm_scope=dm_scope
                )
        elif session_key is None and session_id is None:
            session_key = build_agent_main_session_key(self.agent_id)

        # Look up or create session ID
        if session_key and session_key in self._session_map:
            session_id = self._session_map[session_key]
        else:
            # Generate new session ID if not provided or invalid
            if session_id is None or not self.validate_session_id(session_id):
                session_id = self.generate_session_id()

            # Store mapping if we have a session key
            if session_key:
                self._session_map[session_key] = session_id
                self._save_session_map()
                logger.info(f"Created new session: {session_key} -> {session_id}")

        # Get or create session instance
        if session_id not in self._sessions:
            self._sessions[session_id] = Session(session_id, self.workspace_dir)

        return self._sessions[session_id]

    def get_session(self, session_id: str) -> Session:
        """
        Get or create a session (legacy method)

        Args:
            session_id: Unique session identifier

        Returns:
            Session instance
        """
        if session_id not in self._sessions:
            self._sessions[session_id] = Session(session_id, self.workspace_dir)
        return self._sessions[session_id]

    def list_sessions(self) -> list[str]:
        """
        List all session IDs

        Returns:
            List of session IDs
        """
        sessions_dir = self.workspace_dir / ".sessions"
        if not sessions_dir.exists():
            return []

        session_ids = []
        for f in sessions_dir.glob("*.json"):
            if f.name != "session_map.json":  # Exclude session map file
                session_ids.append(f.stem)

        return sorted(session_ids)

    def get_session_key_for_id(self, session_id: str) -> str | None:
        """Get session key for given session ID."""
        for key, sid in self._session_map.items():
            if sid == session_id:
                return key
        return None

    def list_sessions_by_channel(self, channel: str) -> dict[str, str]:
        """List all sessions for a specific channel."""
        sessions = {}
        for key, sid in self._session_map.items():
            parsed = parse_agent_session_key(key)
            if parsed and channel in parsed.rest:
                sessions[key] = sid
        return sessions

    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session

        Args:
            session_id: Session to delete

        Returns:
            True if deleted, False if not found
        """
        # Remove from memory
        if session_id in self._sessions:
            del self._sessions[session_id]

        # Remove from session map
        keys_to_remove = [k for k, v in self._session_map.items() if v == session_id]
        for key in keys_to_remove:
            del self._session_map[key]

        if keys_to_remove:
            self._save_session_map()
            logger.info(f"Removed {len(keys_to_remove)} session key(s) for {session_id}")

        # Remove from disk
        session_file = self.workspace_dir / ".sessions" / f"{session_id}.json"
        if session_file.exists():
            session_file.unlink()
            return True

        return False

    def get_all_sessions(self) -> list[Session]:
        """
        Get all sessions

        Returns:
            List of Session instances
        """
        session_ids = self.list_sessions()
        return [self.get_session(sid) for sid in session_ids]

    def cleanup_old_sessions(self, max_age_days: int = 30) -> int:
        """
        Delete sessions older than max_age_days

        Args:
            max_age_days: Maximum age in days

        Returns:
            Number of sessions deleted
        """
        from datetime import timedelta

        cutoff = datetime.utcnow() - timedelta(days=max_age_days)
        deleted = 0

        for session in self.get_all_sessions():
            try:
                updated = datetime.fromisoformat(session.updated_at.replace("Z", "+00:00"))
                if updated < cutoff:
                    if self.delete_session(session.session_id):
                        deleted += 1
            except Exception:
                pass

        return deleted
