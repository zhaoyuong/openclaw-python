"""Skill types and structures"""

from typing import Any, Optional
from pydantic import BaseModel


class SkillMetadata(BaseModel):
    """Skill metadata from frontmatter"""

    name: str
    description: Optional[str] = None
    version: Optional[str] = None
    author: Optional[str] = None
    tags: list[str] = []
    requires_bins: list[str] = []
    requires_env: list[str] = []
    requires_config: list[str] = []
    os: Optional[list[str]] = None  # ["darwin", "linux", "windows"]


class Skill(BaseModel):
    """A skill entry"""

    name: str
    content: str  # The skill prompt content
    metadata: SkillMetadata
    source: str  # "bundled", "managed", "workspace", "plugin"
    path: str  # File path


class SkillInvocationPolicy(BaseModel):
    """Skill invocation policy"""

    user_invocable: bool = True
    disable_model_invocation: bool = False
