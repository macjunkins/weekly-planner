"""Shared utilities for configuration and priority formatting.

This module provides lightweight helpers that were originally shared with
``portfolio-manager``. Functions are intentionally minimal to keep the
weekly-planner self contained while matching the expectations of existing
tests and documentation.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


# Priority to emoji mapping used throughout reporting utilities.
_PRIORITY_EMOJIS: dict[str, str] = {
    "critical": "🚨",
    "high": "⚡",
    "medium": "📈",
    "low": "🟡",
}


def load_config(path: str | Path) -> dict[str, Any]:
    """Load the YAML configuration file.

    Args:
        path: Path to the YAML configuration file.

    Returns:
        Parsed configuration as a dictionary.

    Raises:
        FileNotFoundError: If the file does not exist.
        yaml.YAMLError: If the YAML content is invalid.
    """

    config_path = Path(path)
    with config_path.open("r", encoding="utf-8") as config_file:
        return yaml.safe_load(config_file) or {}


def get_priority_emoji(priority: str | None) -> str:
    """Return an emoji representing the given priority level.

    Unknown priorities return a question mark to make the status explicit.

    Args:
        priority: Priority string such as ``"critical"`` or ``"high"``.

    Returns:
        Emoji for the priority if known, otherwise ``"❓"``.
    """

    if priority is None:
        return "❓"

    return _PRIORITY_EMOJIS.get(priority.lower(), "❓")
