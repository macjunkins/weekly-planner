"""Common project utilities for configuration and formatting.

This module is a lightweight replacement for the shared utilities used by
`weekly-planner` and related tools. It focuses on configuration loading and
priority formatting needed by the current test suite.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_config(config_path: str | Path) -> dict[str, Any]:
    """Load a YAML configuration file.

    Args:
        config_path: Path to the YAML configuration file.

    Returns:
        Parsed configuration as a dictionary.

    Raises:
        FileNotFoundError: If the provided path does not exist.
        yaml.YAMLError: If the file cannot be parsed as valid YAML.

    Examples:
        >>> config = load_config("config.yaml")
        >>> isinstance(config, dict)
        True
    """

    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def get_priority_emoji(priority: str) -> str:
    """Return an emoji representing the provided priority level.

    Args:
        priority: Priority string such as "critical", "high", "medium", or
            "low".

    Returns:
        An emoji indicating urgency. Defaults to a bullet if the priority is
        unrecognized.

    Examples:
        >>> get_priority_emoji("critical")
        '🔥'
        >>> get_priority_emoji("medium")
        '➡️'
    """

    normalized = priority.strip().lower()
    mapping = {
        "critical": "🔥",
        "high": "⬆️",
        "medium": "➡️",
        "low": "⬇️",
    }
    return mapping.get(normalized, "•")
