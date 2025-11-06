# Repository Guidelines

## Project Structure & Module Organization
- Core code lives in `lib/`, shared with `portfolio-manager`; add new modules beside `github_client.py` and `project_utils.py`.
- CLI entry points and utilities belong in `scripts/` (see `scripts/weekly_planner.py`).
- Specifications and planning docs sit under `docs/`; keep implementation plans in `docs/` or `AGENTS.md`.
- Tests live in `tests/`; standalone smoke checks are `test_setup.py` and `test_lib.py` in the repo root.

## Build, Test, and Development Commands
- `pip install -r requirements.txt` — install all Python dependencies (3.11+ recommended).
- `python3 test_setup.py` — verify environment, dependency, and symlink health.
- `python3 test_lib.py` — ensure shared library imports and config parsing work.
- `./run_tests.sh` — run both verification scripts with formatted output; use before pushing.

## Coding Style & Naming Conventions
- Follow PEP 8 (4-space indentation, snake_case functions, PascalCase classes).
- Adopt Google-style docstrings with examples, matching current fixtures (`test_setup.py`, issue specs).
- All public functions require type hints; prefer `list[str]`/`dict[str, Any]` style typing (Python 3.10+ syntax).
- Keep modules small and focused; place cross-cutting helpers in `lib/project_utils.py`.

## Testing Guidelines
- Unit and integration tests should target `tests/` with filenames like `test_<module>.py`.
- Prefer `pytest`-compatible structures (plain asserts); align with existing standalone scripts when adding coverage.
- Ensure new modules expose deterministic behavior so `test_lib.py`-style checks remain stable.
- Run `./run_tests.sh` locally before opening a pull request; add targeted tests for new functionality.

## Commit & Pull Request Guidelines
- Match the concise, action-oriented commit style already used (`Fix config paths: …`, `Initial commit: …`).
- Reference GitHub issues in commit bodies or PR descriptions (`Fixes #1`) when applicable.
- Pull requests should include: summary of changes, testing results (`./run_tests.sh` output), and screenshots or sample output if UI/markdown artifacts change.

## Environment & Configuration Tips
- Maintain the `lib` symlink (`ln -s ../portfolio-manager/lib lib`) if it breaks during setup.
- Keep `config.yaml` paths accurate to your local workspace; avoid hardcoding personal directories in code.
