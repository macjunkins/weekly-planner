# Testing Weekly Planner

Quick guide to verify the weekly-planner repository is working correctly.

## Setup Verification

Run the setup verification script to check that all dependencies and configuration are correct:

```bash
python3 test_setup.py
```

This checks:
- ✓ All Python dependencies are installed
- ✓ Configuration files exist and are valid
- ✓ Shared library symlink is working
- ✓ `.env` file exists

**Expected output:** Green "Status: Ready" panel

## Library Integration Test

Run the library integration test to verify that the symlinked shared libraries work correctly:

```bash
python3 test_lib.py
```

This demonstrates:
- ✓ Importing shared utilities from portfolio-manager
- ✓ Loading and parsing YAML configuration
- ✓ Accessing project data for planning
- ✓ Using shared formatting utilities

**Expected output:**
- Tables showing all projects grouped by pillar
- Configuration statistics
- Green "Status: Verified" panel

## Quick Test

Run the comprehensive test suite (both tests with formatted output):

```bash
./run_tests.sh
```

Or run both tests manually:

```bash
python3 test_setup.py && python3 test_lib.py
```

## Troubleshooting

### Missing Dependencies

If you see missing packages:

```bash
pip install -r requirements.txt
```

### Missing .env File

If `.env` is not found:

```bash
cp .env.example .env
# Edit .env and add your GitHub token
```

### Broken lib/ Symlink

If the `lib/` directory is not working:

```bash
# Remove broken symlink if it exists
rm -rf lib

# Create new symlink to portfolio-manager
ln -s ../portfolio-manager/lib lib
```

**Note:** This assumes `portfolio-manager` is in the same parent directory as `weekly-planner`.

## What These Tests DON'T Do

These test scripts verify the **setup and configuration only**. They do NOT:

- Test the actual weekly planning functionality (M1-M5)
- Make any GitHub API calls
- Generate weekly plans or stream schedules
- Create ICS files or markdown outputs

Those features are still in development (see [README.md](README.md) for milestones).

## Development Status

As of November 2025:
- ✅ Repository structure
- ✅ Configuration files
- ✅ Shared library integration
- ✅ Dependency management
- 🚧 M1: Foundation & Data Gathering (in progress)
- ⏳ M2-M5: Not started

See [README.md](README.md) for the full roadmap.
