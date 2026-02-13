"""Terminal UI for OpenClaw.

Interactive terminal chat interface.
"""
from __future__ import annotations

from .tui_app import OpenClawTUI, run_tui

__all__ = ["OpenClawTUI", "run_tui"]

from __future__ import annotations

from .tui import TUI, run_tui
from .types import TUIOptions

__all__ = [
    "TUI",
    "run_tui",
    "TUIOptions",
]
