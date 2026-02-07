"""Tests for tool policy system (matching TS tool-policy.ts)"""

import pytest

from openclaw.security.tool_policy import (
    OWNER_ONLY_TOOL_NAMES,
    TOOL_GROUPS,
    TOOL_NAME_ALIASES,
    TOOL_PROFILES,
    SandboxMode,
    ToolPolicy,
    ToolPolicyResolver,
    ToolProfilePolicy,
    apply_owner_only_tool_policy,
    expand_tool_groups,
    get_profile_policy,
    is_owner_only_tool_name,
    normalize_tool_list,
    normalize_tool_name,
    resolve_tool_profile_policy,
)


class TestToolNameAliases:
    def test_exec_to_bash(self):
        assert normalize_tool_name("exec") == "bash"

    def test_read_to_read_file(self):
        assert normalize_tool_name("read") == "read_file"

    def test_write_to_write_file(self):
        assert normalize_tool_name("write") == "write_file"

    def test_edit_to_edit_file(self):
        assert normalize_tool_name("edit") == "edit_file"

    def test_apply_dash_patch(self):
        assert normalize_tool_name("apply-patch") == "apply_patch"

    def test_no_alias(self):
        assert normalize_tool_name("bash") == "bash"
        assert normalize_tool_name("web_search") == "web_search"

    def test_case_insensitive(self):
        assert normalize_tool_name("EXEC") == "bash"
        assert normalize_tool_name("Read") == "read_file"


class TestNormalizeToolList:
    def test_basic(self):
        result = normalize_tool_list(["exec", "read", "bash"])
        assert result == ["bash", "read_file", "bash"]

    def test_none(self):
        assert normalize_tool_list(None) == []

    def test_empty(self):
        assert normalize_tool_list([]) == []


class TestToolGroups:
    def test_all_groups_present(self):
        expected = [
            "group:memory",
            "group:web",
            "group:fs",
            "group:runtime",
            "group:sessions",
            "group:ui",
            "group:automation",
            "group:messaging",
            "group:nodes",
            "group:openclaw",
        ]
        for group in expected:
            assert group in TOOL_GROUPS, f"Missing group: {group}"

    def test_fs_group(self):
        assert "read_file" in TOOL_GROUPS["group:fs"]
        assert "write_file" in TOOL_GROUPS["group:fs"]
        assert "edit_file" in TOOL_GROUPS["group:fs"]
        assert "apply_patch" in TOOL_GROUPS["group:fs"]

    def test_runtime_group(self):
        assert "bash" in TOOL_GROUPS["group:runtime"]
        assert "process" in TOOL_GROUPS["group:runtime"]

    def test_sessions_group(self):
        assert "sessions_list" in TOOL_GROUPS["group:sessions"]
        assert "sessions_spawn" in TOOL_GROUPS["group:sessions"]
        assert "session_status" in TOOL_GROUPS["group:sessions"]


class TestExpandToolGroups:
    def test_expand_fs(self):
        result = expand_tool_groups(["group:fs"])
        assert "read_file" in result
        assert "write_file" in result
        assert "edit_file" in result
        assert "apply_patch" in result

    def test_expand_mixed(self):
        result = expand_tool_groups(["group:fs", "group:runtime", "image"])
        assert "read_file" in result
        assert "bash" in result
        assert "image" in result

    def test_dedup(self):
        result = expand_tool_groups(["group:fs", "read_file"])
        assert result.count("read_file") == 1

    def test_none(self):
        assert expand_tool_groups(None) == []

    def test_alias_in_group(self):
        # "exec" should resolve to "bash" via alias, then not be a group
        result = expand_tool_groups(["exec"])
        assert "bash" in result


class TestToolProfiles:
    def test_minimal(self):
        p = TOOL_PROFILES["minimal"]
        assert p.allow == ["session_status"]

    def test_coding(self):
        p = TOOL_PROFILES["coding"]
        assert "group:fs" in p.allow
        assert "group:runtime" in p.allow
        assert "image" in p.allow

    def test_messaging(self):
        p = TOOL_PROFILES["messaging"]
        assert "group:messaging" in p.allow

    def test_full(self):
        p = TOOL_PROFILES["full"]
        assert p.allow is None
        assert p.deny is None


class TestResolveToolProfilePolicy:
    def test_minimal(self):
        policy = resolve_tool_profile_policy("minimal")
        assert policy is not None
        assert "session_status" in policy.allow

    def test_full(self):
        policy = resolve_tool_profile_policy("full")
        assert policy is None  # No restrictions

    def test_unknown(self):
        assert resolve_tool_profile_policy("nonexistent") is None

    def test_none(self):
        assert resolve_tool_profile_policy(None) is None


class TestOwnerOnlyTools:
    def test_whatsapp_login(self):
        assert is_owner_only_tool_name("whatsapp_login")

    def test_regular_tool(self):
        assert not is_owner_only_tool_name("bash")
        assert not is_owner_only_tool_name("read_file")


class TestApplyOwnerOnlyToolPolicy:
    class FakeTool:
        def __init__(self, name):
            self.name = name

    def test_owner_keeps_all(self):
        tools = [self.FakeTool("bash"), self.FakeTool("whatsapp_login")]
        result = apply_owner_only_tool_policy(tools, True)
        assert len(result) == 2

    def test_non_owner_filters(self):
        tools = [self.FakeTool("bash"), self.FakeTool("whatsapp_login")]
        result = apply_owner_only_tool_policy(tools, False)
        assert len(result) == 1
        assert result[0].name == "bash"


class TestToolPolicy:
    def test_allow_all(self):
        p = ToolPolicy()
        assert p.is_allowed("anything")

    def test_deny(self):
        p = ToolPolicy(deny=["bash"])
        assert not p.is_allowed("bash")
        assert p.is_allowed("read_file")

    def test_allow_list(self):
        p = ToolPolicy(allow=["bash", "read_file"])
        assert p.is_allowed("bash")
        assert not p.is_allowed("web_search")

    def test_deny_precedence(self):
        p = ToolPolicy(allow=["bash"], deny=["bash"])
        assert not p.is_allowed("bash")

    def test_wildcard(self):
        p = ToolPolicy(allow=["*"])
        assert p.is_allowed("anything")

    def test_group_expansion(self):
        p = ToolPolicy(allow=["group:fs"])
        assert p.is_allowed("read_file")
        assert p.is_allowed("write_file")
        assert not p.is_allowed("bash")

    def test_alias_resolution(self):
        p = ToolPolicy(deny=["bash"])
        # "exec" normalizes to "bash"
        assert not p.is_allowed("exec")


class TestToolPolicyResolver:
    def test_global_deny(self):
        resolver = ToolPolicyResolver(
            {
                "tools": {"deny": ["browser"]},
            }
        )
        allowed, reason = resolver.is_tool_allowed("browser", "main")
        assert not allowed
        assert "denied" in reason

    def test_global_allow(self):
        resolver = ToolPolicyResolver(
            {
                "tools": {"allow": ["bash"]},
            }
        )
        allowed, _ = resolver.is_tool_allowed("bash", "main")
        assert allowed

    def test_agent_specific(self):
        resolver = ToolPolicyResolver(
            {
                "agents": {
                    "myagent": {"tools": {"deny": ["web_search"]}},
                },
            }
        )
        allowed, _ = resolver.is_tool_allowed("web_search", "myagent")
        assert not allowed

    def test_sandbox_mode(self):
        resolver = ToolPolicyResolver(
            {
                "agents": {
                    "defaults": {
                        "sandbox": {
                            "mode": "non-main",
                            "tools": {"allow": ["bash"]},
                        },
                    },
                },
            }
        )
        # Main session: no sandbox
        allowed, _ = resolver.is_tool_allowed("web_search", "agent", is_main_session=True)
        assert allowed

        # Non-main session: sandbox applies
        allowed, _ = resolver.is_tool_allowed("web_search", "agent", is_main_session=False)
        assert not allowed


class TestGetProfilePolicy:
    def test_ts_profiles(self):
        for name in ("minimal", "coding", "messaging"):
            p = get_profile_policy(name)
            assert p is not None

    def test_full_returns_none_restriction(self):
        # "full" has no restrictions, so expanded policy is empty
        p = get_profile_policy("full")
        assert p is None  # full → resolve returns None

    def test_legacy_profiles(self):
        for name in ("safe", "restricted"):
            p = get_profile_policy(name)
            assert p is not None

    def test_unknown(self):
        assert get_profile_policy("nonexistent") is None
