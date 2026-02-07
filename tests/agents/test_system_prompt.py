"""Tests for system prompt builder"""

from pathlib import Path

import pytest

from openclaw.agents.system_prompt import (
    build_agent_system_prompt,
    format_skills_for_prompt,
)
from openclaw.agents.system_prompt_sections import SILENT_REPLY_TOKEN


class TestBuildAgentSystemPrompt:
    """Test main system prompt builder"""

    def test_full_mode_basic(self, tmp_path):
        prompt = build_agent_system_prompt(
            workspace_dir=tmp_path,
            tool_names=["read_file", "write_file", "bash"],
            prompt_mode="full",
        )
        assert "## Tooling" in prompt
        assert "## Tool Call Style" in prompt
        assert "## Safety" in prompt
        assert "## OpenClaw CLI Quick Reference" in prompt
        assert "## Workspace" in prompt
        assert "## Silent Replies" in prompt
        assert SILENT_REPLY_TOKEN in prompt

    def test_full_mode_all_params(self, tmp_path):
        prompt = build_agent_system_prompt(
            workspace_dir=tmp_path,
            tool_names=["read_file", "write_file", "message", "memory_search"],
            skills_prompt="<available_skills><skill><name>t</name></skill></available_skills>",
            heartbeat_prompt="ping",
            docs_path="/docs",
            prompt_mode="full",
            runtime_info={"agent_id": "test", "host": "h", "model": "m", "channel": "telegram"},
            user_timezone="America/New_York",
            owner_numbers=["+1234567890"],
            extra_system_prompt="Group chat context.",
            context_files=[
                {"path": "AGENTS.md", "content": "Guidelines"},
                {"path": "SOUL.md", "content": "Friendly"},
            ],
            model_alias_lines=["- opus: claude-opus-4"],
            tts_hint="Use tts for voice.",
            reaction_guidance={"level": "minimal", "channel": "telegram"},
            reasoning_level="on",
            reasoning_hint="Use <thinking> tags.",
            has_gateway=True,
        )

        # 26 sections check
        for marker in [
            "## Tooling",
            "## Tool Call Style",
            "## Safety",
            "## OpenClaw CLI Quick Reference",
            "## Skills",
            "## Memory Recall",
            "## OpenClaw Self-Update",
            "## Model Aliases",
            "## Workspace",
            "## Documentation",
            "## User Identity",
            "## Current Date & Time",
            "## Workspace Files (injected)",
            "## Reply Tags",
            "## Messaging",
            "## Voice (TTS)",
            "## Group Chat Context",
            "## Reactions",
            "## Reasoning Format",
            "# Project Context",
            "## Silent Replies",
            "## Heartbeats",
            "## Runtime",
        ]:
            assert marker in prompt, f"Missing: {marker}"

        assert "embody its persona" in prompt  # SOUL.md detection

    def test_minimal_mode(self, tmp_path):
        prompt = build_agent_system_prompt(
            workspace_dir=tmp_path,
            tool_names=["read_file"],
            skills_prompt="<skills/>",
            heartbeat_prompt="ping",
            prompt_mode="minimal",
            has_gateway=True,
        )
        assert "## Safety" in prompt
        assert "## Tooling" in prompt
        assert "## Skills" not in prompt
        assert "## Memory" not in prompt
        assert "## Silent Replies" not in prompt
        assert "## Heartbeats" not in prompt
        assert "## Self-Update" not in prompt
        assert "## Reply Tags" not in prompt

    def test_none_mode(self, tmp_path):
        prompt = build_agent_system_prompt(workspace_dir=tmp_path, prompt_mode="none")
        assert prompt == "You are a personal assistant running inside OpenClaw."

    def test_safety_always_included(self, tmp_path):
        for mode in ("full", "minimal"):
            prompt = build_agent_system_prompt(workspace_dir=tmp_path, prompt_mode=mode)
            assert "## Safety" in prompt

    def test_soul_md_detection(self, tmp_path):
        prompt_with = build_agent_system_prompt(
            workspace_dir=tmp_path,
            context_files=[{"path": "SOUL.md", "content": "Friendly"}],
        )
        prompt_without = build_agent_system_prompt(
            workspace_dir=tmp_path,
            context_files=[{"path": "AGENTS.md", "content": "Guidelines"}],
        )
        assert "embody its persona" in prompt_with
        assert "embody its persona" not in prompt_without

    def test_extra_system_prompt_headers(self, tmp_path):
        full = build_agent_system_prompt(
            workspace_dir=tmp_path,
            prompt_mode="full",
            extra_system_prompt="Context",
        )
        assert "## Group Chat Context" in full

        minimal = build_agent_system_prompt(
            workspace_dir=tmp_path,
            prompt_mode="minimal",
            extra_system_prompt="Context",
        )
        assert "## Subagent Context" in minimal


class TestFormatSkillsForPrompt:
    def test_basic(self):
        prompt = format_skills_for_prompt(
            [
                {"name": "github", "description": "GitHub CLI", "location": "/path/SKILL.md"},
            ]
        )
        assert "<available_skills>" in prompt
        assert "<name>github</name>" in prompt

    def test_multiple(self):
        prompt = format_skills_for_prompt(
            [
                {"name": "a", "description": "A", "location": "/a"},
                {"name": "b", "description": "B", "location": "/b", "tags": ["x", "y"]},
            ]
        )
        assert prompt.count("<skill>") == 2
        assert "<tags>x, y</tags>" in prompt

    def test_empty(self):
        assert format_skills_for_prompt([]) == ""


class TestPromptLength:
    def test_not_excessive(self, tmp_path):
        prompt = build_agent_system_prompt(
            workspace_dir=tmp_path,
            tool_names=["read_file", "bash"],
            prompt_mode="full",
        )
        assert 1000 < len(prompt) < 50000

    def test_minimal_shorter(self, tmp_path):
        full = build_agent_system_prompt(
            workspace_dir=tmp_path,
            tool_names=["read_file"],
            skills_prompt="<s/>",
            prompt_mode="full",
        )
        minimal = build_agent_system_prompt(
            workspace_dir=tmp_path,
            tool_names=["read_file"],
            skills_prompt="<s/>",
            prompt_mode="minimal",
        )
        assert len(minimal) < len(full)
