"""Configuration loading and persistence"""

import os
import json
from pathlib import Path
from typing import Optional
import pyjson5

from .schema import ClawdbotConfig


def get_config_path() -> Path:
    """Get the config file path"""
    config_dir = Path.home() / ".clawdbot"
    config_dir.mkdir(exist_ok=True)
    return config_dir / "clawdbot.json"


def load_config(config_path: Optional[Path] = None) -> ClawdbotConfig:
    """Load configuration from file or return defaults"""
    if config_path is None:
        config_path = get_config_path()

    if not config_path.exists():
        # Return default config
        return ClawdbotConfig()

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            # Support JSON5 for comments
            config_data = pyjson5.load(f)
        return ClawdbotConfig(**config_data)
    except Exception as e:
        print(f"Warning: Failed to load config from {config_path}: {e}")
        print("Using default configuration")
        return ClawdbotConfig()


def save_config(config: ClawdbotConfig, config_path: Optional[Path] = None) -> None:
    """Save configuration to file"""
    if config_path is None:
        config_path = get_config_path()

    config_path.parent.mkdir(parents=True, exist_ok=True)

    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config.model_dump(exclude_none=True), f, indent=2)
