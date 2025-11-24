"""Utility helpers for weekly-planner.

Provides configuration loading and priority formatting helpers shared across
scripts and tests.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_config(path: str | Path) -> dict[str, Any]:
    """Load YAML configuration from ``path``.

    Args:
        path: Location of the YAML configuration file.

    Returns:
        Parsed configuration as a dictionary.

    Raises:
        FileNotFoundError: If ``path`` does not exist.
        yaml.YAMLError: If YAML cannot be parsed.
    """
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with config_path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def get_priority_emoji(priority: str) -> str:
    """Return an emoji representing the given priority level.

    Args:
        priority: Priority label (e.g., ``critical``, ``high``, ``medium``).

    Returns:
        Emoji string to visually represent the priority. Defaults to a pin for
        unknown priorities.
    """
    normalized = priority.lower()
    mapping = {
        "critical": "🔥",
        "high": "⚡",
        "medium": "📌",
        "low": "🟢",
    }
    return mapping.get(normalized, "📌")
