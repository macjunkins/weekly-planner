"""Time estimation utilities for GitHub issues.

This module parses time estimates from issue descriptions using
configurable regex patterns defined in ``config.yaml``.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Iterable, Optional

import yaml


class TimeEstimator:
    """Parse time estimates from GitHub issue bodies.

    Examples:
        >>> estimator = TimeEstimator()
        >>> estimator.extract_estimate("Estimate: 2 hours")
        2
        >>> estimator.extract_estimate("[4h] Implement feature")
        4
        >>> estimator.extract_estimate("No estimate provided")
        1
    """

    def __init__(self, config_path: Optional[Path | str] = None) -> None:
        """Initialize the estimator and compile patterns.

        Args:
            config_path: Optional path to a YAML config file. Defaults to
                ``config.yaml`` at the repository root.
        """
        config_file = Path(config_path) if config_path else Path(__file__).resolve().parent.parent / "config.yaml"
        config = self._load_config(config_file)

        self.default_hours: int = int(config.get("default_estimate_hours", 1))
        self.max_hours: int = int(config.get("max_estimate_hours", 8))
        pattern_strings: Iterable[str] = config.get("estimate_patterns", [])
        self.patterns = [re.compile(pattern) for pattern in pattern_strings]

    @staticmethod
    def _load_config(config_path: Path) -> dict[str, Any]:
        """Load time estimation configuration from YAML.

        Args:
            config_path: Path to the configuration file.

        Returns:
            Dictionary containing the weekly planner configuration block.
        """
        with config_path.open("r", encoding="utf-8") as handle:
            config = yaml.safe_load(handle)
        return config.get("weekly_planner", {}) if isinstance(config, dict) else {}

    def extract_estimate(self, issue_body: Optional[str]) -> int:
        """Extract a time estimate from an issue description.

        Args:
            issue_body: Issue description text or ``None``.

        Returns:
            Parsed hours clamped between ``default_hours`` and ``max_hours``.
        """
        if not issue_body or not issue_body.strip():
            return self.default_hours

        for pattern in self.patterns:
            match = pattern.search(issue_body)
            if not match:
                continue

            hours = self._normalize_hours(match.group(1))
            if hours is not None:
                return hours

        return self.default_hours

    def batch_extract(self, issues: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Extract estimates for multiple issues.

        Args:
            issues: List of issue dictionaries containing at least a
                ``body`` field.

        Returns:
            New list of issue dictionaries augmented with ``estimated_hours``.
        """
        results: list[dict[str, Any]] = []
        for issue in issues:
            if not isinstance(issue, dict):
                continue  # Skip non-dict items
            body = issue.get("body")
            estimated_hours = self.extract_estimate(body if body is None or isinstance(body, str) else str(body))

            updated_issue = dict(issue)
            updated_issue["estimated_hours"] = estimated_hours
            results.append(updated_issue)
        return results

    def _normalize_hours(self, value: str) -> Optional[int]:
        """Normalize matched hour string into a bounded integer.

        Args:
            value: Captured numeric value from regex.

        Returns:
            Normalized integer within allowed bounds, or ``None`` if invalid.
        """
        try:
            hours = abs(int(value))
        except (TypeError, ValueError):
            return None

        if hours == 0:
            return self.default_hours

        return min(hours, self.max_hours)


__all__ = ["TimeEstimator"]
