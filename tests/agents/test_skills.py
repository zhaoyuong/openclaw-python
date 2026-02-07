"""
Tests for skills system

Matches TypeScript skills test structure
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from openclaw.agents.skills import (
    build_workspace_skills_prompt,
    load_skills_from_dir,
    load_workspace_skill_entries,
)


class TestSkillLoader:
    """Tests for skill loading."""

    def test_load_skills_from_empty_dir(self):
        """Test loading from empty directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skills = load_skills_from_dir(Path(tmpdir))
            assert skills == []

    def test_load_single_skill(self):
        """Test loading a single skill."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)

            # Create skill directory and SKILL.md
            skill_dir = tmpdir_path / "test-skill"
            skill_dir.mkdir()

            skill_file = skill_dir / "SKILL.md"
            skill_file.write_text("""---
name: test-skill
description: A test skill
---

# Test Skill

This is a test skill.
""")

            skills = load_skills_from_dir(tmpdir_path)

            assert len(skills) == 1
            assert skills[0].name == "test-skill"
            assert skills[0].description == "A test skill"
            assert "SKILL.md" in skills[0].location

    def test_skill_name_from_directory(self):
        """Test skill name defaults to directory name."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)

            skill_dir = tmpdir_path / "my-skill"
            skill_dir.mkdir()

            skill_file = skill_dir / "SKILL.md"
            skill_file.write_text("""# My Skill

Description here.
""")

            skills = load_skills_from_dir(tmpdir_path)

            assert len(skills) == 1
            assert skills[0].name == "my-skill"


class TestWorkspaceSkills:
    """Tests for workspace skills management."""

    def test_load_workspace_skills(self):
        """Test loading skills from workspace."""
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            skills_dir = workspace / "skills"
            skills_dir.mkdir()

            # Create a skill
            skill_dir = skills_dir / "summarize"
            skill_dir.mkdir()

            skill_file = skill_dir / "SKILL.md"
            skill_file.write_text("""---
name: summarize
description: Summarize text or files
---

# Summarize Skill

Usage instructions...
""")

            entries = load_workspace_skill_entries(workspace)

            assert len(entries) == 1
            assert entries[0].skill.name == "summarize"
            assert entries[0].skill.description == "Summarize text or files"

    def test_build_workspace_skills_prompt(self):
        """Test building skills prompt."""
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            skills_dir = workspace / "skills"
            skills_dir.mkdir()

            # Create a skill
            skill_dir = skills_dir / "test-skill"
            skill_dir.mkdir()

            skill_file = skill_dir / "SKILL.md"
            skill_file.write_text("""---
name: test-skill
description: Test description
---

# Test Skill
""")

            prompt = build_workspace_skills_prompt(workspace)

            assert "## Available Skills" in prompt
            assert "test-skill" in prompt
            assert "Test description" in prompt
            assert "read_file" in prompt  # Default tool name

    def test_empty_workspace_returns_empty_prompt(self):
        """Test empty workspace returns empty prompt."""
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            prompt = build_workspace_skills_prompt(workspace)
            assert prompt == ""


class TestSkillMetadata:
    """Tests for skill metadata parsing."""

    def test_parse_openclaw_metadata(self):
        """Test parsing OpenClaw metadata from frontmatter."""
        from openclaw.agents.skills.frontmatter import parse_openclaw_metadata

        frontmatter = {
            "openclaw": {
                "always": True,
                "emoji": "📝",
                "primaryEnv": "OPENAI_API_KEY",
                "requires": {"bins": ["jq", "curl"]},
            }
        }

        metadata = parse_openclaw_metadata(frontmatter)

        assert metadata is not None
        assert metadata.always is True
        assert metadata.emoji == "📝"
        assert metadata.primary_env == "OPENAI_API_KEY"
        assert "bins" in metadata.requires
        assert "jq" in metadata.requires["bins"]
