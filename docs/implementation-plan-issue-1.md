# Implementation Plan: Time Estimation Parser (Issue #1)

## Context
- Issue https://github.com/macjunkins/weekly-planner/issues/1 requests `lib/time_estimator.py`.
- Must honor regex patterns and defaults defined in `config.yaml` and reinforced by `docs/functional-requirements.md:95` and `docs/nonfunctional-requirements.md:113`.

## Objectives
- Parse GitHub issue descriptions for estimates using five configurable patterns.
- Return default (1h) when no pattern matches and cap to 8h maximum.
- Provide typed, well-documented API (`TimeEstimator.extract_estimate`, `TimeEstimator.batch_extract`).

## Deliverables
- `lib/time_estimator.py` implementing `TimeEstimator`.
- Unit coverage for edge cases (negative, zero, > max, no match, multiple matches).
- Updated test fixtures if required.

## Work Plan
1. **Config Alignment**
   - Load patterns, defaults from `config.yaml`.
   - Decide ingestion method (direct load vs dependency injection) to keep parser configurable/testable.
2. **API & Parsing Logic**
   - Implement initializer compiling patterns once.
   - Normalize matched hours (int conversion, absolute value guard, clamp to `max_hours`).
   - Determine rule for multiple matches (first match priority).
3. **Batch Operations**
   - Implement `batch_extract` to operate on iterable of issue dicts (`number`, `body`).
   - Handle missing keys gracefully with defaults.
4. **Validation & Docs**
   - Add Google-style docstrings with examples (per issue spec).
   - Ensure type hints consistent across public methods.
5. **Testing**
   - Create unit tests covering happy paths and edge cases (negative input, zero, >8, no match).
   - Validate patterns cover all five configurations from issue body.

## Risks & Mitigations
- **Pattern drift:** Guard by reading patterns from config in tests to detect config changes.
- **Unexpected text formats:** Include trimming and whitespace normalization before matching.
- **Performance on bulk batch:** Precompile regex patterns and avoid repeated config reads.

## Open Questions
- Should batch mode skip or include issues with missing `body` field? (Assume default unless guidance given.)
- Is there an existing config loader utility to reuse for pattern retrieval (e.g., `lib/project_utils.py`)? Review before implementation.
