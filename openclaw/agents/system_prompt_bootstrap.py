"""
Bootstrap file loading and injection

Automatically loads workspace context files (AGENTS.md, SOUL.md, etc.)
and formats them for injection into the system prompt.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import NamedTuple

logger = logging.getLogger(__name__)


class BootstrapFile(NamedTuple):
    """Bootstrap file with metadata"""

    path: str
    content: str
    truncated: bool = False


def load_bootstrap_files(
    workspace_dir: Path, max_chars_per_file: int = 20000
) -> list[BootstrapFile]:
    """
    Load workspace bootstrap files

    Files loaded (in order):
    - AGENTS.md: Project guidelines and conventions
    - SOUL.md: Persona definition
    - TOOLS.md: Tool usage instructions
    - IDENTITY.md: Identity configuration
    - USER.md: User information
    - HEARTBEAT.md: Heartbeat configuration
    - BOOTSTRAP.md: Bootstrap instructions (for new workspaces)

    Args:
        workspace_dir: Workspace directory
        max_chars_per_file: Maximum characters per file (truncate if exceeded)

    Returns:
        List of BootstrapFile objects
    """
    bootstrap_files = [
        "AGENTS.md",
        "SOUL.md",
        "TOOLS.md",
        "IDENTITY.md",
        "USER.md",
        "HEARTBEAT.md",
        "BOOTSTRAP.md",
    ]

    results = []

    for filename in bootstrap_files:
        file_path = workspace_dir / filename

        if not file_path.exists():
            # Inject missing file marker
            results.append(
                BootstrapFile(
                    path=filename,
                    content=f"(File {filename} not found in workspace)",
                    truncated=False,
                )
            )
            continue

        try:
            content = file_path.read_text(encoding="utf-8")

            # Truncate if too long (matching TypeScript behavior: 70% head + 20% tail)
            truncated = False
            if len(content) > max_chars_per_file:
                head_chars = int(max_chars_per_file * 0.7)
                tail_chars = int(max_chars_per_file * 0.2)

                head = content[:head_chars]
                tail = content[-tail_chars:]

                # Add truncation marker
                truncation_marker = (
                    f"\n\n... (truncated: file exceeded {max_chars_per_file} chars; "
                    f"showing first {head_chars} + last {tail_chars} chars) ...\n\n"
                )

                content = head + truncation_marker + tail
                truncated = True

            results.append(BootstrapFile(path=filename, content=content, truncated=truncated))

            if truncated:
                logger.warning(
                    f"Bootstrap file {filename} truncated " f"(exceeded {max_chars_per_file} chars)"
                )
            else:
                logger.debug(f"Loaded bootstrap file {filename} ({len(content)} chars)")

        except Exception as e:
            logger.error(f"Failed to read bootstrap file {filename}: {e}")
            results.append(
                BootstrapFile(
                    path=filename, content=f"(Error reading {filename}: {e})", truncated=False
                )
            )

    return results


def format_bootstrap_context(files: list[BootstrapFile]) -> list[dict]:
    """
    Format bootstrap files as context_files list for system prompt injection

    Args:
        files: List of BootstrapFile objects

    Returns:
        List of dicts with 'path' and 'content' keys (ready for system prompt)
    """
    if not files:
        return []

    context_files = []

    for file in files:
        # Skip missing files (unless we want to show the marker)
        if "(File" in file.content and "not found" in file.content:
            # Optionally skip missing files, or include the marker
            continue

        context_files.append({"path": file.path, "content": file.content})

    return context_files


def format_bootstrap_context_string(files: list[BootstrapFile]) -> str:
    """
    Format bootstrap files as a complete string for legacy injection

    This formats the files the same way as TypeScript's buildBootstrapContextFiles.

    Args:
        files: List of BootstrapFile objects

    Returns:
        Formatted Project Context section as a string
    """
    if not files:
        return ""

    lines = [
        "# Project Context",
        "",
        "The following project context files have been loaded:",
        "",
    ]

    # Check if SOUL.md is present (and not missing)
    has_soul = any(f.path == "SOUL.md" and "(File" not in f.content for f in files)

    if has_soul:
        lines.extend(
            [
                "If SOUL.md is present, embody its persona and tone.",
                "Avoid stiff, generic replies; follow its guidance unless higher-priority instructions override it.",
                "",
            ]
        )

    # Add each file
    for file in files:
        lines.extend(
            [
                f"## {file.path}",
                "",
                file.content,
                "",
            ]
        )

    return "\n".join(lines)
