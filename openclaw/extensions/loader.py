"""Extension loader: discover and load extensions from disk.

Matches pi-mono loader behavior: scan ~/.openclaw/extensions and .openclaw/extensions.
"""
from __future__ import annotations

import importlib.util
import json
import logging
import sys
from pathlib import Path
from typing import Any, Callable

from .api import ExtensionAPI
from .types import ExtensionContext, ExtensionManifest

logger = logging.getLogger(__name__)

MANIFEST_FILENAME = "extension.json"
MAIN_MODULE = "extension.py"


def _extension_dirs(workspace_root: Path | None = None) -> list[Path]:
    """Return directories to scan for extensions (home first, then workspace)."""
    dirs: list[Path] = []
    home = Path.home()
    global_dir = home / ".openclaw" / "extensions"
    if global_dir.is_dir():
        dirs.append(global_dir)
    if workspace_root:
        workspace_ext = workspace_root / ".openclaw" / "extensions"
        if workspace_ext.is_dir() and workspace_ext not in dirs:
            dirs.append(workspace_ext)
    return dirs


def _load_manifest(ext_dir: Path) -> ExtensionManifest | None:
    """Load and parse extension.json from a directory."""
    manifest_path = ext_dir / MANIFEST_FILENAME
    if not manifest_path.is_file():
        return None
    try:
        data = json.loads(manifest_path.read_text())
        return ExtensionManifest(
            name=data.get("name", ext_dir.name),
            version=data.get("version", "0.0.0"),
            description=data.get("description", ""),
            author=data.get("author"),
            main=data.get("main", MAIN_MODULE),
            dependencies=data.get("dependencies", []),
            permissions=data.get("permissions", []),
        )
    except Exception as e:
        logger.warning("Failed to load manifest %s: %s", manifest_path, e)
        return None


def _load_module_from_path(module_name: str, file_path: Path) -> Any:
    """Load a Python module from a file path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {file_path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod


def discover_extensions(
    workspace_root: Path | None = None,
    agent_id: str = "default",
    session_id: str | None = None,
    config: dict[str, Any] | None = None,
) -> list[tuple[Path, ExtensionManifest]]:
    """
    Discover extension directories that contain extension.json and main module.

    Returns list of (extension_dir, manifest).
    """
    found: list[tuple[Path, ExtensionManifest]] = []
    for base in _extension_dirs(workspace_root):
        if not base.is_dir():
            continue
        for ext_dir in base.iterdir():
            if not ext_dir.is_dir():
                continue
            manifest = _load_manifest(ext_dir)
            if manifest is None:
                continue
            main_path = ext_dir / manifest.main
            if not main_path.is_file():
                logger.debug("Extension %s has no main file %s", ext_dir.name, manifest.main)
                continue
            found.append((ext_dir, manifest))
    return found


def load_extension(
    ext_dir: Path,
    manifest: ExtensionManifest,
    context: ExtensionContext,
) -> ExtensionAPI | None:
    """
    Load a single extension: import main module and call register(api).

    Returns the ExtensionAPI after registration (with tools/handlers populated),
    or None on error.
    """
    main_path = ext_dir / manifest.main
    if not main_path.is_file():
        return None
    ext_id = f"{manifest.name}@{manifest.version}"
    api = ExtensionAPI(ext_id, context)
    try:
        mod_name = f"openclaw_ext_{manifest.name.replace('-', '_')}"
        mod = _load_module_from_path(mod_name, main_path)
        if not hasattr(mod, "register"):
            logger.warning("Extension %s has no register(api) function", ext_id)
            return None
        mod.register(api)
        return api
    except Exception as e:
        logger.exception("Failed to load extension %s: %s", ext_id, e)
        return None


class ExtensionLoader:
    """
    Loads all discovered extensions and collects their tools and handlers.
    """

    def __init__(
        self,
        workspace_root: Path | None = None,
        agent_id: str = "default",
        session_id: str | None = None,
        config: dict[str, Any] | None = None,
    ):
        self.workspace_root = workspace_root
        self.agent_id = agent_id
        self.session_id = session_id
        self.config = config or {}
        self._apis: list[ExtensionAPI] = []
        self._errors: list[tuple[str, str]] = []

    def load_all(self) -> list[ExtensionAPI]:
        """Discover and load all extensions. Returns list of ExtensionAPI (after register)."""
        self._apis = []
        self._errors = []
        context = ExtensionContext(
            extension_dir=Path("."),
            agent_id=self.agent_id,
            session_id=self.session_id,
            config=self.config,
        )
        for ext_dir, manifest in discover_extensions(
            self.workspace_root,
            self.agent_id,
            self.session_id,
            self.config,
        ):
            context.extension_dir = ext_dir
            api = load_extension(ext_dir, manifest, context)
            if api is not None:
                self._apis.append(api)
            else:
                self._errors.append((str(ext_dir), "load_extension returned None"))
        return self._apis

    def get_all_tools(self) -> list[dict[str, Any]]:
        """Return all tools from all loaded extensions."""
        tools: list[dict[str, Any]] = []
        for api in self._apis:
            tools.extend(api.get_tools())
        return tools

    def get_all_handlers(self) -> dict[str, list[Callable[..., Any]]]:
        """Merge handlers by event name from all extensions."""
        merged: dict[str, list[Callable[..., Any]]] = {}
        for api in self._apis:
            for event, handlers in api.get_handlers().items():
                merged.setdefault(event, []).extend(handlers)
        return merged

    def get_errors(self) -> list[tuple[str, str]]:
        """Return (path, error) for extensions that failed to load."""
        return self._errors.copy()
