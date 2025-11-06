# Weekly Planner

Automated weekly work planning and stream schedule generation.

## Status

🚧 **In Development** - See milestones for progress

## Overview

Weekly Planner automates the generation of:
- **Weekly work plans** - 5-day schedules with prioritized tasks
- **Stream schedules** - Content planning for live coding streams
- **Calendar exports** - ICS format for calendar integration

The tool analyzes your GitHub issues, roadmaps, and priorities to generate optimized weekly schedules that balance:
- Strategic priorities (revenue, infrastructure, consistency)
- Task dependencies and blockers
- Streamable vs off-stream work
- Time estimates and capacity planning

## Documentation

- [Functional Requirements](docs/functional-requirements.md) - Features and capabilities
- [Non-Functional Requirements](docs/nonfunctional-requirements.md) - Implementation phases and architecture

## Milestones

Development is organized into 5 milestones:

- [ ] **M1: Foundation & Data Gathering** (6-8 hours)
  - Fetch GitHub issues and classify them
  - Parse time estimates and roadmap data
  - Determine streamable vs off-stream tasks

- [ ] **M2: Scheduling Engine** (6-8 hours)
  - Calculate priority scores
  - Pack tasks into 5-day time blocks
  - Handle constraints and dependencies

- [ ] **M3: Output Generation - Work Plan** (6-8 hours)
  - Generate `weekly-plan-YYYY-MM-DD.md` files
  - Create `.ics` calendar files with timezone handling
  - Validate formatting and imports

- [ ] **M4: Stream Plan Integration** (10-12 hours)
  - Generate stream prep folders (5 per week)
  - Create outlines, checklists, YouTube descriptions
  - Integrate with existing `/stream-plan` workflow

- [ ] **M5: CLI & Polish** (8-10 hours)
  - Full CLI interface with arguments
  - Rich console output (progress bars, tables)
  - Error handling and comprehensive docs

**Total estimated effort:** 36-46 hours

## Quick Start

### 1. Install Dependencies

```bash
cd weekly-planner
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and add: GITHUB_TOKEN=your_token_here
```

**Required token scopes:** `repo`, `read:org`, `read:user`

### 3. Verify Setup

Run the comprehensive test suite to ensure everything is working:

```bash
./run_tests.sh
```

You should see "ALL TESTS PASSED - Repository is ready for development!"

See [TESTING.md](TESTING.md) for detailed testing documentation and individual test scripts.

## Installation

### Dependencies

```bash
pip install -r requirements.txt
```

**Required:**
- `gql[all]==3.5.0` - GitHub GraphQL API client
- `PyYAML==6.0.1` - Configuration parsing
- `python-dotenv==1.0.0` - Environment management
- `GitPython==3.1.40` - Git repository operations
- `icalendar>=5.0.0` - ICS calendar generation
- `pytz>=2023.3` - Timezone handling

**Utilities:**
- `python-dateutil==2.8.2` - Date/time utilities
- `rich==13.7.0` - Terminal output formatting

## Configuration

### config.yaml

Edit `config.yaml` to customize your project portfolio:

- **GitHub settings**: Organizations and user to monitor
- **Projects**: Paths, repositories, priorities, and pillars
- **Strategic pillars**: revenue, infrastructure, consistency, cleanup, innovation
- **Reports**: Output directories and formatting preferences
- **Milestones**: Quarterly goals and date ranges

The configuration is shared with [portfolio-manager](https://github.com/macjunkins/portfolio-manager) for consistency.

### Environment Variables

See Quick Start above for `.env` setup. Required token scopes: `repo`, `read:org`, `read:user`

## Usage

Coming soon. Planned CLI interface:

```bash
# Generate weekly plan
weekly-planner generate

# Generate with specific date
weekly-planner generate --start-date 2025-11-04

# Generate stream plans only
weekly-planner generate --streams-only

# Preview without writing files
weekly-planner generate --dry-run
```

## Project Structure

```
weekly-planner/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── config.yaml                        # Project configuration
├── .env.example                       # Environment template
├── .gitignore
├── lib/                               # Symlinked from portfolio-manager
│   ├── github_client.py              # GitHub GraphQL client
│   └── project_utils.py              # Shared utilities
├── scripts/
│   └── weekly_planner.py             # Main entry point (M5)
├── docs/
│   ├── functional-requirements.md
│   └── nonfunctional-requirements.md
└── tests/                            # Unit tests (future)
```

**Note:** The `lib/` directory is symlinked to `../portfolio-manager/lib` for shared utilities.

## Development Roadmap

### Current Phase: M1 - Foundation & Data Gathering

**Next steps:**
1. Implement `lib/time_estimator.py` - Parse time estimates from issue descriptions
2. Implement `lib/task_classifier.py` - Classify streamable vs off-stream tasks
3. Implement `lib/roadmap_parser.py` - Parse meta-roadmap.md
4. Add unit tests for time estimation patterns
5. Validate roadmap parsing logic

See [nonfunctional-requirements.md](docs/nonfunctional-requirements.md) for detailed phase breakdown.

## Integration with Portfolio Manager

Weekly Planner shares utilities with [portfolio-manager](https://github.com/macjunkins/portfolio-manager):
- GitHub GraphQL client
- Project configuration parsing
- Health scoring and status tracking

This allows both tools to use consistent data sources and reduce code duplication.

## Migration History

This repository was created from the `personal-scripts` monorepo on 2025-11-02.

**Previous location:** `/Users/johnjunkins/GitHub/personal-scripts/` (specification documents only)
**New home:** `https://github.com/macjunkins/weekly-planner`

**Changes:**
- Separated weekly-planner specifications into dedicated repository
- Added symlink to shared utilities from portfolio-manager
- Added weekly-planner specific dependencies (icalendar, pytz)

## Contributing

This is a personal automation tool. If you'd like to use it:

1. Fork the repository
2. Update `config.yaml` with your projects
3. Generate your own `.env` file
4. Adjust paths and settings as needed

## Author

**John Junkins** (@macjunkins)

**Created:** 2025-11-02
**Status:** 🚧 In Development (M1 starting)
**Estimated completion:** Q1 2026
