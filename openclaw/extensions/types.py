"""Extension type definitions

Extensions run IN the agent runtime, not the gateway.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Protocol


@dataclass
class ExtensionManifest:
    """Extension manifest (extension.json)"""
    name: str
    version: str
    description: str
    author: str | None = None
    main: str = "extension.py"
    dependencies: list[str] = field(default_factory=list)
    permissions: list[str] = field(default_factory=list)


@dataclass
class ExtensionContext:
    """Context passed to extensions"""
    extension_dir: Path
    agent_id: str
    session_id: str | None = None
    config: dict[str, Any] = field(default_factory=dict)


class Extension(Protocol):
    """
    Extension protocol
    
    Extensions must implement:
    - register(api: ExtensionAPI) -> None
    """
    
    def register(self, api: "ExtensionAPI") -> None:
        """Register extension capabilities"""
        ...
