"""Time estimation utilities for GitHub issues.

The :class:`TimeEstimator` parses issue bodies for time estimates using
patterns defined in ``config.yaml``. Estimates are normalized, clamped to a
maximum, and available via single-issue and batch APIs.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from project_utils import load_config


@dataclass
class TimeEstimatorConfig:
    """Configuration values for :class:`TimeEstimator`."""

    patterns: list[str]
    default_hours: int
    max_hours: int


class TimeEstimator:
    """Parse GitHub issue bodies for time estimates.

    The estimator loads regex patterns from ``config.yaml`` under
    ``weekly_planner.estimate_patterns``. Patterns are compiled once during
    initialization for performance.

    Examples:
        >>> estimator = TimeEstimator()
        >>> estimator.extract_estimate("Estimate: 3 hours")
        3
        >>> estimator.batch_extract([{"number": 1, "body": "[2h]"}])[0]["estimated_hours"]
        2
    """

    def __init__(self) -> None:
        config = self._load_config()
        self._patterns = [re.compile(pattern) for pattern in config.patterns]
        self._default_hours = config.default_hours
        self._max_hours = config.max_hours

    @property
    def patterns(self) -> list[re.Pattern[str]]:
        """Compiled regex patterns used to extract estimates."""

        return self._patterns

    @property
    def default_hours(self) -> int:
        """Default estimate (in hours) returned when no pattern matches."""

        return self._default_hours

    @property
    def max_hours(self) -> int:
        """Maximum allowed estimate (in hours)."""

        return self._max_hours

    def extract_estimate(self, issue_body: Optional[str]) -> int:
        """Extract a time estimate from a single issue body.

        Args:
            issue_body: The body text of a GitHub issue.

        Returns:
            Estimated hours as an integer. If no pattern matches, returns the
            configured default. Values are normalized to be positive and clamped
            to ``max_hours``.
        """

        if not issue_body:
            return self._default_hours

        for pattern in self._patterns:
            match = pattern.search(issue_body)
            if match:
                try:
                    hours = int(match.group(1))
                except (IndexError, ValueError):
                    continue

                normalized = abs(hours)
                if normalized == 0:
                    return self._default_hours

                return min(normalized, self._max_hours)

        return self._default_hours

    def batch_extract(self, issues: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Extract estimates for a list of issues.

        Args:
            issues: List of issue dictionaries that may contain a ``body`` key.

        Returns:
            New list of issues with an ``estimated_hours`` field added. Original
            issue dictionaries are not mutated.
        """

        results: list[dict[str, Any]] = []
        for issue in issues:
            body = issue.get("body") if isinstance(issue, dict) else None
            estimate = self.extract_estimate(body if isinstance(body, str) else None)
            enriched = {**issue, "estimated_hours": estimate}
            results.append(enriched)

        return results

    def _load_config(self) -> TimeEstimatorConfig:
        """Load estimator configuration from ``config.yaml``."""

        config_path = Path(__file__).resolve().parent.parent / "config.yaml"
        config = load_config(config_path)
        planner_config = config.get("weekly_planner", {})

        patterns = planner_config.get("estimate_patterns", [])
        default_hours = int(planner_config.get("default_estimate_hours", 1))
        max_hours = int(planner_config.get("max_estimate_hours", 8))

        return TimeEstimatorConfig(
            patterns=patterns,
            default_hours=default_hours,
            max_hours=max_hours,
        )
