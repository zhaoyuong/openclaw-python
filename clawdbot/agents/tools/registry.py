"""Tool registry"""

from typing import Optional
from .base import AgentTool
from .bash import BashTool
from .file_ops import ReadFileTool, WriteFileTool, EditFileTool
from .web import WebFetchTool, WebSearchTool


class ToolRegistry:
    """Registry of available tools"""

    def __init__(self):
        self._tools: dict[str, AgentTool] = {}
        self._register_default_tools()

    def _register_default_tools(self) -> None:
        """Register default tools"""
        # File operations
        self.register(ReadFileTool())
        self.register(WriteFileTool())
        self.register(EditFileTool())

        # Process execution
        self.register(BashTool())

        # Web tools
        self.register(WebFetchTool())
        self.register(WebSearchTool())

    def register(self, tool: AgentTool) -> None:
        """Register a tool"""
        self._tools[tool.name] = tool

    def get(self, name: str) -> Optional[AgentTool]:
        """Get tool by name"""
        return self._tools.get(name)

    def list_tools(self) -> list[AgentTool]:
        """List all tools"""
        return list(self._tools.values())

    def get_tools_by_profile(self, profile: str = "full") -> list[AgentTool]:
        """Get tools filtered by profile"""
        # TODO: Implement profile-based filtering
        if profile == "minimal":
            return [self.get("read_file"), self.get("web_fetch")]
        elif profile == "coding":
            return [
                self.get("read_file"),
                self.get("write_file"),
                self.get("edit_file"),
                self.get("bash"),
                self.get("web_fetch")
            ]
        elif profile == "messaging":
            return [self.get("web_fetch"), self.get("web_search")]
        else:  # full
            return self.list_tools()


# Global tool registry
_global_registry = ToolRegistry()


def get_tool_registry() -> ToolRegistry:
    """Get global tool registry"""
    return _global_registry
