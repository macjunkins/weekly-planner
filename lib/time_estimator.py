"""Time estimation utilities for GitHub issues.

The :class:`TimeEstimator` reads configured regex patterns from ``config.yaml``
and extracts estimated hours from issue bodies. When no valid estimate is
found, it falls back to the configured default. Values are clamped to the
configured maximum to avoid unrealistic schedules.

Example:
    >>> estimator = TimeEstimator()
    >>> estimator.extract_estimate("Estimate: 3 hours")
    3
    >>> estimator.batch_extract([
    ...     {"number": 1, "body": "Estimate: 2h"},
    ...     {"number": 2, "body": "No estimate"},
    ... ])
    [{'number': 1, 'body': 'Estimate: 2h', 'estimated_hours': 2},
     {'number': 2, 'body': 'No estimate', 'estimated_hours': 1}]
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from project_utils import load_config


class TimeEstimator:
    """Parse and normalize time estimates from issue bodies.

    Patterns, defaults, and maximums are loaded from ``config.yaml`` under the
    ``weekly_planner`` key. The patterns are compiled once during
    initialization for efficient reuse.
    """

    def __init__(self) -> None:
        config_path = Path(__file__).parent.parent / "config.yaml"
        config = load_config(config_path)
        planner_config = config.get("weekly_planner", {})

        pattern_strings = planner_config.get("estimate_patterns", [])
        self.patterns = [re.compile(pattern) for pattern in pattern_strings]
        self.default_hours = int(planner_config.get("default_estimate_hours", 1))
        self.max_hours = int(planner_config.get("max_estimate_hours", 8))

    def extract_estimate(self, issue_body: str | None) -> int:
        """Extract an hour estimate from an issue body.

        Args:
            issue_body: The text content of the issue body.

        Returns:
            Normalized hour estimate. Falls back to the configured default when
            no pattern matches or when invalid values are encountered.
        """
        if issue_body is None:
            return self.default_hours

        text = issue_body.strip()
        if not text:
            return self.default_hours

        for pattern in self.patterns:
            match = pattern.search(text)
            if not match:
                continue

            value = int(match.group(1))
            normalized = abs(value)
            if normalized == 0:
                return self.default_hours

            if normalized > self.max_hours:
                return self.max_hours

            return normalized

        return self.default_hours

    def batch_extract(self, issues: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Extract estimates for a batch of issues.

        Args:
            issues: List of issue dictionaries containing at least a ``body``
                field.

        Returns:
            New list of issue dictionaries with an added ``estimated_hours``
            field while preserving the original data.
        """
        results: list[dict[str, Any]] = []
        for issue in issues:
            if not isinstance(issue, dict):
                continue  # Skip non-dict items
            body = issue.get("body")
            estimate = self.extract_estimate(body)
            enriched_issue = dict(issue)
            enriched_issue["estimated_hours"] = estimate
            results.append(enriched_issue)
        return results
