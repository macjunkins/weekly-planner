"""Time estimation utilities for GitHub issues.

The :class:`TimeEstimator` reads estimation patterns from ``config.yaml``
so that tests and future CLI commands can consistently parse issue
bodies. Estimates default to a minimum value and are clamped to a
configurable maximum to avoid unrealistic schedules.
"""
from __future__ import annotations

from pathlib import Path
import re
from typing import Any, Optional

from project_utils import load_config

# Default patterns mirror the ones defined in config.yaml so the class
# remains functional even if configuration cannot be loaded.
DEFAULT_PATTERNS: list[str] = [
    r"(?i)estimated?:\s*(\d+)\s*(?:hours?|hrs?|h)",
    r"(?i)time:\s*(\d+)\s*(?:hours?|hrs?|h)",
    r"(?i)effort:\s*(\d+)\s*(?:hours?|hrs?|h)",
    r"\[(\d+)h\]",
    r"\[(\d+)\s*hours?\]",
]
DEFAULT_ESTIMATE_HOURS = 1
DEFAULT_MAX_HOURS = 8


class TimeEstimator:
    """Extract time estimates from GitHub issue bodies.

    Patterns and defaults are configured via the ``weekly_planner``
    section of ``config.yaml``.
    """

    def __init__(self, config_path: Optional[str | Path] = None) -> None:
        self.config_path = Path(config_path) if config_path else Path(__file__).parent.parent / "config.yaml"
        config = self._load_config()

        patterns = config.get("weekly_planner", {}).get("estimate_patterns", DEFAULT_PATTERNS)
        self.patterns = [re.compile(pattern) for pattern in patterns]
        self.default_hours = int(config.get("weekly_planner", {}).get("default_estimate_hours", DEFAULT_ESTIMATE_HOURS))
        self.max_hours = int(config.get("weekly_planner", {}).get("max_estimate_hours", DEFAULT_MAX_HOURS))

        # Validate configuration: default_hours must not exceed max_hours
        if self.default_hours > self.max_hours:
            raise ValueError(
                f"Configuration error: default_estimate_hours ({self.default_hours}) "
                f"must not exceed max_estimate_hours ({self.max_hours})"
            )

    def _load_config(self) -> dict[str, Any]:
        """Load configuration safely with sensible fallbacks."""

        try:
            return load_config(self.config_path)
        except FileNotFoundError:
            return {"weekly_planner": {}}

    def extract_estimate(self, issue_body: Optional[str]) -> int:
        """Extract a time estimate from an issue body.

        Args:
            issue_body: Raw issue description or ``None``.

        Returns:
            Estimated hours between ``default_hours`` and ``max_hours``.
        """

        if not issue_body or not issue_body.strip():
            return self.default_hours

        normalized_body = issue_body.strip()

        for pattern in self.patterns:
            match = pattern.search(normalized_body)
            if match:
                try:
                    hours = abs(int(match.group(1)))
                except (TypeError, ValueError):
                    continue

                if hours == 0:
                    return self.default_hours

                return min(max(hours, self.default_hours), self.max_hours)

        return self.default_hours

    def batch_extract(self, issues: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Extract time estimates for a batch of issues.

        Args:
            issues: List of issue dictionaries containing a ``body`` field.

        Returns:
            New list of dictionaries, preserving the original fields and
            adding ``estimated_hours`` for each issue.
        """

        results: list[dict[str, Any]] = []
        for issue in issues:
            issue_copy = issue.copy()
            issue_copy["estimated_hours"] = self.extract_estimate(issue.get("body"))
            results.append(issue_copy)
        return results


__all__ = ["TimeEstimator"]
