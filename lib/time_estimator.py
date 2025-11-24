"""Time estimation parsing for GitHub issues.

The :class:`TimeEstimator` reads regex patterns from ``config.yaml`` and uses
them to extract time estimates expressed in hours from issue bodies. It supports
five pattern styles defined in configuration and provides both single-item and
batch extraction helpers.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Iterable, Optional

from project_utils import load_config


class TimeEstimator:
    """Parse time estimates from GitHub issue bodies.

    Estimates are discovered using compiled regular expressions specified in
    ``config.yaml`` under ``weekly_planner.estimate_patterns``. Extracted values
    are normalized to integers, clamped to ``max_estimate_hours``, and fall back
    to ``default_estimate_hours`` when no valid match is found.

    Examples:
        >>> estimator = TimeEstimator()
        >>> estimator.extract_estimate("Estimate: 3 hours")
        3
        >>> estimator.extract_estimate("[2h] Build feature")
        2
    """

    def __init__(self, config_path: Optional[str | Path] = None) -> None:
        """Initialize the estimator and compile regex patterns.

        Args:
            config_path: Optional path to an alternate configuration file.
                Defaults to ``config.yaml`` in the repository root.
        """

        root_path = Path(__file__).parent.parent
        self._config_path = Path(config_path) if config_path else root_path / "config.yaml"
        config = load_config(self._config_path)
        weekly_config = config.get("weekly_planner", {})

        self._pattern_strings: list[str] = list(weekly_config.get("estimate_patterns", []))
        self._patterns = [re.compile(pattern) for pattern in self._pattern_strings]
        self._default_hours = int(weekly_config.get("default_estimate_hours", 1))
        self._max_hours = int(weekly_config.get("max_estimate_hours", 8))

    @property
    def patterns(self) -> list[Any]:
        """Return compiled regex patterns."""

        return self._patterns

    @property
    def default_hours(self) -> int:
        """Return the default number of hours when no match is found."""

        return self._default_hours

    @property
    def max_hours(self) -> int:
        """Return the maximum number of hours allowed for a single issue."""

        return self._max_hours

    def extract_estimate(self, issue_body: Optional[str]) -> int:
        """Extract a time estimate from a single issue body.

        Args:
            issue_body: The text body of the issue or ``None``.

        Returns:
            Estimated hours as an integer. Returns ``default_hours`` when no
            match is found, when the body is missing, or when the parsed value
            is zero or negative. Values greater than ``max_hours`` are clamped.
        """

        if issue_body is None:
            return self._default_hours

        normalized_body = issue_body.strip()
        if not normalized_body:
            return self._default_hours

        for pattern in self._patterns:
            match = pattern.search(normalized_body)
            if not match:
                continue

            raw_value = match.group(1)
            hours = abs(int(raw_value))

            if hours == 0:
                return self._default_hours

            return min(hours, self._max_hours)

        return self._default_hours

    def batch_extract(self, issues: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
        """Extract time estimates for a collection of issues.

        Args:
            issues: Iterable of dictionaries that include a ``body`` field.

        Returns:
            A list of dictionaries with an added ``estimated_hours`` key while
            preserving all original keys.
        """

        results: list[dict[str, Any]] = []
        for issue in issues:
            body = issue.get("body") if isinstance(issue, dict) else None
            estimated = self.extract_estimate(body if isinstance(body, str) or body is None else str(body))
            enriched_issue = dict(issue)
            enriched_issue["estimated_hours"] = estimated
            results.append(enriched_issue)

        return results
