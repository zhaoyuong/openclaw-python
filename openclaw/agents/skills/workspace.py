"""
Workspace skills management

Loads and merges skills from multiple sources.
Matches TypeScript src/agents/skills/workspace.ts
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from .loader import format_skills_for_prompt, load_skill_entries_from_dir
from .types import SkillEntry, SkillSnapshot

logger = logging.getLogger(__name__)


def get_openclaw_dir() -> Path:
    """Get OpenClaw config directory (~/.openclaw/)."""
    return Path.home() / ".openclaw"


def get_managed_skills_dir() -> Path:
    """Get managed skills directory (~/.openclaw/skills/)."""
    return get_openclaw_dir() / "skills"


def load_workspace_skill_entries(
    workspace_dir: Path | str,
    config: Any | None = None,
    managed_skills_dir: Path | None = None,
    bundled_skills_dir: Path | None = None,
) -> list[SkillEntry]:
    """
    Load skills from all sources (matches TS loadWorkspaceSkillEntries).

    Priority (highest first):
    1. Workspace skills ({workspace}/skills/)
    2. Managed skills (~/.openclaw/skills/)
    3. Plugin skills (if configured)
    4. Extra dirs (from config)
    5. Bundled skills

    Args:
        workspace_dir: Workspace directory
        config: OpenClaw configuration
        managed_skills_dir: Optional managed skills directory
        bundled_skills_dir: Optional bundled skills directory

    Returns:
        List of SkillEntry objects, deduplicated by name
    """
    if isinstance(workspace_dir, str):
        workspace_dir = Path(workspace_dir)

    # Determine directories
    if managed_skills_dir is None:
        managed_skills_dir = get_managed_skills_dir()

    workspace_skills_dir = workspace_dir / "skills"

    # Load from different sources
    bundled_entries = []
    if bundled_skills_dir and bundled_skills_dir.exists():
        bundled_entries = load_skill_entries_from_dir(bundled_skills_dir, source="openclaw-bundled")

    # Extra dirs from config
    extra_entries = []
    if config:
        extra_dirs = get_extra_skill_dirs(config)
        for extra_dir in extra_dirs:
            extra_entries.extend(load_skill_entries_from_dir(extra_dir, source="openclaw-extra"))

    # Managed skills
    managed_entries = []
    if managed_skills_dir.exists():
        managed_entries = load_skill_entries_from_dir(managed_skills_dir, source="openclaw-managed")

    # Workspace skills (highest priority)
    workspace_entries = []
    if workspace_skills_dir.exists():
        workspace_entries = load_skill_entries_from_dir(workspace_skills_dir, source="workspace")

    # Merge with priority (later sources override earlier)
    entries_by_name: dict[str, SkillEntry] = {}

    for entry in bundled_entries + extra_entries + managed_entries + workspace_entries:
        entries_by_name[entry.skill.name] = entry

    return list(entries_by_name.values())


def build_workspace_skills_prompt(
    workspace_dir: Path | str,
    config: Any | None = None,
    read_tool_name: str = "read_file",
    skill_filter: list[str] | None = None,
) -> str:
    """
    Build skills prompt for system prompt (matches TS buildWorkspaceSkillsPrompt).

    Args:
        workspace_dir: Workspace directory
        config: OpenClaw configuration
        read_tool_name: Name of read tool to reference
        skill_filter: Optional list of skill names to include

    Returns:
        Formatted skills prompt section
    """
    if isinstance(workspace_dir, str):
        workspace_dir = Path(workspace_dir)

    entries = load_workspace_skill_entries(workspace_dir, config)

    # Apply filter if provided
    if skill_filter is not None:
        normalized = [name.strip() for name in skill_filter if name.strip()]
        if normalized:
            entries = [e for e in entries if e.skill.name in normalized]

    if not entries:
        return ""

    skills = [entry.skill for entry in entries]
    skills_list = format_skills_for_prompt(skills)

    return f"""## Available Skills

Skills are located in the workspace `skills/` directory:

{skills_list}

Usage:
- If exactly one skill clearly applies: read its SKILL.md at <location> with `{read_tool_name}`, then follow it.
- If multiple skills might apply: ask user which to use.
- If none clearly apply: do not read any SKILL.md.
"""


def build_workspace_skill_snapshot(
    workspace_dir: Path | str,
    config: Any | None = None,
) -> SkillSnapshot:
    """
    Build skill snapshot (matches TS buildWorkspaceSkillSnapshot).

    Args:
        workspace_dir: Workspace directory
        config: OpenClaw configuration

    Returns:
        SkillSnapshot
    """
    if isinstance(workspace_dir, str):
        workspace_dir = Path(workspace_dir)

    entries = load_workspace_skill_entries(workspace_dir, config)
    skills = [entry.skill for entry in entries]

    prompt = format_skills_for_prompt(skills)

    skill_info = []
    for entry in entries:
        info = {"name": entry.skill.name}
        if entry.metadata and entry.metadata.primary_env:
            info["primaryEnv"] = entry.metadata.primary_env
        skill_info.append(info)

    return SkillSnapshot(prompt=prompt, skills=skill_info, resolved_skills=skills, version=1)


def filter_workspace_skill_entries(
    entries: list[SkillEntry],
    config: Any | None = None,
    skill_filter: list[str] | None = None,
) -> list[SkillEntry]:
    """
    Filter skill entries (matches TS filterWorkspaceSkillEntries).

    Args:
        entries: Skill entries to filter
        config: OpenClaw configuration
        skill_filter: Optional list of skill names to include

    Returns:
        Filtered skill entries
    """
    filtered = entries

    # Apply skill filter
    if skill_filter is not None:
        normalized = [name.strip() for name in skill_filter if name.strip()]
        if normalized:
            filtered = [e for e in filtered if e.skill.name in normalized]

    # Apply config-based filtering (if needed)
    # TODO: Implement config-based filtering

    return filtered


def get_extra_skill_dirs(config: Any) -> list[Path]:
    """
    Get extra skill directories from config.

    Args:
        config: OpenClaw configuration

    Returns:
        List of Path objects
    """
    if not config:
        return []

    # Try to get extra dirs from config
    try:
        if hasattr(config, "skills") and hasattr(config.skills, "load"):
            extra_dirs = getattr(config.skills.load, "extraDirs", [])
            if extra_dirs:
                return [Path(d).expanduser() for d in extra_dirs if d]
    except Exception:
        pass

    return []
