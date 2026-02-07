"""
Skills system for OpenClaw

Matches TypeScript src/agents/skills/
"""

from .loader import load_skills_from_dir
from .types import OpenClawSkillMetadata, Skill, SkillEntry, SkillSnapshot
from .workspace import (
    build_workspace_skill_snapshot,
    build_workspace_skills_prompt,
    load_workspace_skill_entries,
)

__all__ = [
    "Skill",
    "SkillEntry",
    "SkillSnapshot",
    "OpenClawSkillMetadata",
    "load_skills_from_dir",
    "load_workspace_skill_entries",
    "build_workspace_skills_prompt",
    "build_workspace_skill_snapshot",
]
