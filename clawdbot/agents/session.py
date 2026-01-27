"""Session management for agent conversations"""

import json
from pathlib import Path
from typing import Any, Optional
from datetime import datetime
from pydantic import BaseModel


class Message(BaseModel):
    """A single message in a conversation"""

    role: str  # "user", "assistant", "tool"
    content: str
    timestamp: str = ""
    tool_calls: Optional[list[dict[str, Any]]] = None
    tool_call_id: Optional[str] = None

    def __init__(self, **data: Any):
        if "timestamp" not in data or not data["timestamp"]:
            data["timestamp"] = datetime.utcnow().isoformat() + "Z"
        super().__init__(**data)


class Session:
    """Manages a conversation session"""

    def __init__(self, session_id: str, workspace_dir: Optional[Path] = None):
        self.session_id = session_id
        self.messages: list[Message] = []
        self.metadata: dict[str, Any] = {}

        # Set up workspace directory
        if workspace_dir is None:
            workspace_dir = Path.home() / ".clawdbot" / "sessions"
        self.workspace_dir = workspace_dir
        self.session_dir = self.workspace_dir / session_id
        self.session_dir.mkdir(parents=True, exist_ok=True)

        # Session file path
        self.session_file = self.session_dir / "transcript.jsonl"

        # Load existing session if available
        self._load()

    def _load(self) -> None:
        """Load session from disk"""
        if not self.session_file.exists():
            return

        try:
            with open(self.session_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        msg_data = json.loads(line)
                        self.messages.append(Message(**msg_data))
        except Exception as e:
            print(f"Warning: Failed to load session {self.session_id}: {e}")

    def _save_message(self, message: Message) -> None:
        """Append message to session file"""
        with open(self.session_file, "a", encoding="utf-8") as f:
            f.write(message.model_dump_json() + "\n")

    def add_message(self, role: str, content: str, **kwargs: Any) -> Message:
        """Add a message to the session"""
        message = Message(role=role, content=content, **kwargs)
        self.messages.append(message)
        self._save_message(message)
        return message

    def add_user_message(self, content: str) -> Message:
        """Add a user message"""
        return self.add_message("user", content)

    def add_assistant_message(self, content: str, tool_calls: Optional[list[dict[str, Any]]] = None) -> Message:
        """Add an assistant message"""
        return self.add_message("assistant", content, tool_calls=tool_calls)

    def add_tool_message(self, tool_call_id: str, content: str) -> Message:
        """Add a tool result message"""
        return self.add_message("tool", content, tool_call_id=tool_call_id)

    def get_messages(self, limit: Optional[int] = None) -> list[Message]:
        """Get messages from the session"""
        if limit is None:
            return self.messages
        return self.messages[-limit:]

    def clear(self) -> None:
        """Clear the session"""
        self.messages = []
        if self.session_file.exists():
            self.session_file.unlink()

    def to_dict(self) -> dict[str, Any]:
        """Convert session to dictionary"""
        return {
            "sessionId": self.session_id,
            "messageCount": len(self.messages),
            "messages": [msg.model_dump() for msg in self.messages],
            "metadata": self.metadata
        }


class SessionManager:
    """Manages multiple sessions"""

    def __init__(self, workspace_dir: Optional[Path] = None):
        if workspace_dir is None:
            workspace_dir = Path.home() / ".clawdbot" / "sessions"
        self.workspace_dir = workspace_dir
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
        self._sessions: dict[str, Session] = {}

    def get_session(self, session_id: str) -> Session:
        """Get or create a session"""
        if session_id not in self._sessions:
            self._sessions[session_id] = Session(session_id, self.workspace_dir)
        return self._sessions[session_id]

    def list_sessions(self) -> list[str]:
        """List all session IDs"""
        if not self.workspace_dir.exists():
            return []

        sessions = []
        for session_dir in self.workspace_dir.iterdir():
            if session_dir.is_dir():
                sessions.append(session_dir.name)
        return sessions

    def delete_session(self, session_id: str) -> None:
        """Delete a session"""
        if session_id in self._sessions:
            del self._sessions[session_id]

        session_dir = self.workspace_dir / session_id
        if session_dir.exists():
            import shutil
            shutil.rmtree(session_dir)
