"""Base tool interface"""

from abc import ABC, abstractmethod
from typing import Any, Optional
from pydantic import BaseModel


class ToolResult(BaseModel):
    """Result from tool execution"""

    success: bool
    content: str
    error: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None


class AgentTool(ABC):
    """Base class for agent tools"""

    def __init__(self):
        self.name: str = ""
        self.description: str = ""

    @abstractmethod
    def get_schema(self) -> dict[str, Any]:
        """Get JSON schema for tool parameters"""
        pass

    @abstractmethod
    async def execute(self, params: dict[str, Any]) -> ToolResult:
        """Execute the tool with given parameters"""
        pass

    def to_dict(self) -> dict[str, Any]:
        """Convert tool to dictionary representation"""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.get_schema()
        }
