"""Shared project utilities for weekly-planner.

These helpers mirror the lightweight utilities from the shared
portfolio-manager toolkit so tests can import them without the
external symlink. Functions include configuration loading and
priority formatting helpers used throughout the project.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


_DEFAULT_PRIORITY_EMOJIS: dict[str, str] = {
    "critical": "🔥",
    "high": "⚡",
    "medium": "✅",
    "low": "🕐",
}


def load_config(config_path: str | Path) -> dict[str, Any]:
    """Load a YAML configuration file and return the parsed data.

    Args:
        config_path: Path to the YAML configuration file.

    Returns:
        Parsed configuration dictionary.

    Raises:
        FileNotFoundError: If the provided config file does not exist.
        yaml.YAMLError: If the YAML contents cannot be parsed.
    """

    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def get_priority_emoji(priority: str) -> str:
    """Return a friendly emoji for a given priority level.

    Unknown priorities fall back to a neutral bullet.
    """

    return _DEFAULT_PRIORITY_EMOJIS.get(priority.lower(), "•")


__all__ = ["load_config", "get_priority_emoji"]
