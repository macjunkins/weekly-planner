# Weekly Planner - Non-Functional Requirements

**Created:** 2025-11-01
**Owner:** John Junkins (@macjunkins)
**Status:** Design Phase
**Implementation Target:** 2025-11-02+

---

## Overview

This document describes implementation details, quality attributes, configuration, and operational requirements for the Weekly Planner script.

---

## Configuration

**Extended `config.yaml`:**

```yaml
# ... existing configuration ...

weekly_planner:
  # Work schedule
  work_days_per_week: 5  # Mon-Fri
  total_hours_per_day: 6

  # Stream configuration
  stream_hours_per_day: 4
  stream_time_cst: "13:00-17:00"  # 1 PM - 5 PM
  stream_days:
    - monday
    - tuesday
    - wednesday
    - thursday
    - friday

  # Off-stream work
  off_stream_hours_per_day: 2
  off_stream_flexible: true  # Can be done anytime

  # Time estimation
  estimate_patterns:
    - "(?i)estimate[d]?:\\s*(\\d+)\\s*(?:hours?|hrs?|h)"
    - "(?i)time:\\s*(\\d+)\\s*(?:hours?|hrs?|h)"
    - "(?i)effort:\\s*(\\d+)\\s*(?:hours?|hrs?|h)"
    - "\\[(\\d+)h\\]"
    - "\\[(\\d+)\\s*hours?\\]"
  default_estimate_hours: 1
  max_estimate_hours: 8  # Sanity check

  # Task classification
  streamable_label: "streamable"

  # Prioritization weights
  pillar_weights:
    revenue: 10
    infrastructure: 7
    consistency: 5
    innovation: 3
    cleanup: 1

  urgency_multipliers:
    blocking: 10
    due_this_week: 8
    due_next_2_weeks: 5
    due_this_month: 4
    no_deadline: 3

  importance_multipliers:
    critical_path: 10
    decision_gate: 8
    milestone: 6
    normal: 4
    low: 2

  # Context switching
  prefer_single_project_per_day: true
  max_projects_per_day: 2

  # Output configuration
  output_dir: "docs/plans"
  markdown_template: "weekly-plan"

  # Calendar settings
  timezone: "America/Chicago"
  calendar_reminder_minutes: [30, 5]  # Two reminders
  calendar_location: "Rumble"

  # Stream plan integration (NEW)
  generate_stream_plans: true                              # Auto-generate stream folders
  streaming_repo_path: "/Users/johnjunkins/Projects/Streaming"
  stream_plans_output_dir: "streams"                       # Relative to streaming_repo_path
  stream_duration_hours: 4                                 # 4-hour streams (not 3)

  # Milestone grouping preferences
  prefer_milestone_grouping: true                          # Group tasks by milestone when possible
  milestone_grouping_threshold: 3                          # Min hours from same milestone to group

  # Meta-roadmap
  meta_roadmap_path: "/Users/johnjunkins/Projects/meta-roadmap.md"
  current_quarter: "Q1"  # Auto-detect from date
  current_year: 2026
```

---

## Implementation Plan

### Phase 1: Core Infrastructure (Day 1)

**Files to create:**
1. `lib/time_estimator.py`
   - Parse time estimates from issue descriptions
   - Handle multiple pattern formats
   - Validate and cap estimates

2. `lib/task_classifier.py`
   - Check for `streamable` label
   - Classify into stream vs off-stream buckets

3. `lib/roadmap_parser.py`
   - Parse `meta-roadmap.md`
   - Extract current quarter priorities
   - Identify upcoming decision gates
   - Parse "Quick Reference: Next Actions"

**Tests:**
- Unit tests for time estimation patterns
- Validation of roadmap parsing

---

### Phase 2: Scheduling Logic (Day 2)

**Files to create:**
1. `lib/prioritizer.py`
   - Calculate priority scores
   - Apply pillar weights, urgency, importance
   - Sort tasks by score

2. `lib/time_packer.py`
   - Pack tasks into 4-hour stream blocks
   - Pack tasks into 2-hour off-stream blocks
   - Minimize context switching
   - Handle overflow/underflow

**Tests:**
- Prioritization score calculations
- Time packing edge cases (too many tasks, too few tasks)

---

### Phase 3: Output Generation (Day 3)

**Files to create:**
1. `lib/schedule_builder.py`
   - Generate markdown sections
   - Build day-by-day structure
   - Format task lists
   - Include stream plan folder references

2. `lib/ics_generator.py`
   - Generate ICS format
   - Handle timezone conversion (CST → UTC)
   - Add reminders
   - Include task details and stream plan paths in descriptions

**Tests:**
- Markdown formatting validation
- ICS format validation (import into test calendar)

---

### Phase 3.5: Stream Plan Generation (Day 3.5)

**Files to create:**
1. `lib/stream_planner.py`
   - Extract stream plan generation logic from `/stream-plan` slash command
   - Functions:
     - `generate_stream_outline()` - Create hour-by-hour guide
     - `generate_pre_stream_checklist()` - Pre-flight checklist
     - `generate_youtube_description()` - Video description
     - `generate_social_media_posts()` - Twitter/Discord posts
     - `create_stream_folder()` - Create folder in Streaming/streams/
   - Support both automated (weekly planner) and interactive (slash command) modes
   - Reusable for both workflows (DRY principle)

**Integration Points:**
- `weekly_planner.py` calls `stream_planner` for each streaming day
- `/stream-plan` slash command refactored to use same functions
- Single source of truth for stream plan generation logic

**Milestone Grouping Logic:**
```python
def group_tasks_by_milestone(tasks: list, target_hours: int = 4) -> dict:
    """
    Group tasks by milestone, preferring cohesive streams.

    Strategy:
    1. Group all tasks by milestone
    2. For each milestone with enough tasks to fill target_hours, prefer it
    3. Fall back to priority-based packing if no good milestone fit
    """
    milestones = {}
    for task in tasks:
        milestone = task.get('milestone', 'No Milestone')
        if milestone not in milestones:
            milestones[milestone] = []
        milestones[milestone].append(task)

    # Calculate total hours per milestone
    milestone_hours = {
        m: sum(t['hours'] for t in tasks)
        for m, tasks in milestones.items()
    }

    # Find milestones that can fill a day (within threshold)
    viable_milestones = {
        m: tasks for m, tasks in milestones.items()
        if 3 <= milestone_hours[m] <= 5  # 3-5 hour range for 4-hour target
    }

    return viable_milestones
```

**Tests:**
- Test stream plan file generation
- Verify folder structure and file contents
- Test with/without milestone data
- Verify timezone handling in social posts

---

### Phase 4: Main Script & Integration (Day 4)

**Files to create:**
1. `scripts/weekly_planner.py`
   - CLI argument parsing
   - Orchestrate all modules
   - Error handling
   - Progress output (rich console)

**Integration:**
- Reuse `lib/github_client.py` from `portfolio_status.py`
- Reuse `lib/project_utils.py` from `portfolio_status.py`
- Load `config.yaml` configuration

**Tests:**
- End-to-end test with sample data
- Verify file outputs

---

### Phase 5: Polish & Documentation (Day 5)

**Tasks:**
1. Add rich console output (progress bars, tables)
2. Write comprehensive docstrings
3. Add error messages for common issues
4. Create usage examples
5. Update `README.md` in `personal-scripts/`

---

## Dependencies

**Existing:**
- `lib/github_client.py` (from `portfolio_status.py`)
- `lib/project_utils.py` (from `portfolio_status.py`)
- `config.yaml` (extended with new settings)

**Shared with `/stream-plan` slash command:**
- `lib/stream_planner.py` is used by both:
  - `weekly_planner.py` (automated batch generation)
  - `/stream-plan` slash command (interactive single stream)
- Maintains DRY principle (single source of truth)
- Any updates to stream plan format apply to both workflows

**New Python packages:**
```
icalendar>=5.0.0  # ICS generation
pytz>=2023.3      # Timezone handling
```

**Add to `requirements.txt`:**
```
# ... existing packages ...
icalendar>=5.0.0
pytz>=2023.3
```

---

## Edge Cases to Handle

### 1. Not Enough Streamable Tasks
**Problem:** Less than 4 hours of streamable work available
**Solution:**
- Fill remainder with "flex time" or "polish/refactor"
- Suggest creating more issues with `streamable` label
- Mark stream as "open-ended exploration"

### 2. Too Many High-Priority Tasks
**Problem:** More than 30 hours of critical work
**Solution:**
- Warn user about overload
- Show overflow tasks in "Deferred to Next Week" section
- Suggest extending plan to 2 weeks

### 3. No Time Estimates on Issues
**Problem:** Many issues missing time estimates
**Solution:**
- Use default 1-hour estimate
- Generate warning report listing issues without estimates
- Suggest adding estimates to improve planning

### 4. Context Switching Overload
**Problem:** Tasks spread across too many projects
**Solution:**
- Force grouping by project
- Defer lower-priority projects to future weeks
- Limit to 2 projects per stream day max

### 5. Milestone Due Dates Past
**Problem:** Overdue milestones creating artificial urgency
**Solution:**
- Flag overdue milestones separately
- Don't inflate urgency score for very old deadlines
- Suggest milestone date updates

### 6. Timezone Confusion (DST)
**Problem:** Daylight Saving Time transitions
**Solution:**
- Use `pytz` for proper DST handling
- Always store in CST (America/Chicago)
- Convert correctly to UTC for ICS

---

## Technical Notes

### Timezone Handling

```python
import pytz
from datetime import datetime

# Define CST timezone
cst = pytz.timezone('America/Chicago')

# Stream start time: 1 PM CST
stream_start = datetime(2025, 11, 4, 13, 0, 0)
stream_start_cst = cst.localize(stream_start)

# Convert to UTC for ICS
stream_start_utc = stream_start_cst.astimezone(pytz.UTC)

# ICS format: YYYYMMDDTHHmmssZ
ics_datetime = stream_start_utc.strftime('%Y%m%dT%H%M%SZ')
# Result: 20251104T190000Z (7 PM UTC = 1 PM CST in non-DST)
```

### ICS Generation

```python
from icalendar import Calendar, Event, Alarm
from datetime import datetime, timedelta

cal = Calendar()
cal.add('prodid', '-//macjunkins//Weekly Planner//EN')
cal.add('version', '2.0')

event = Event()
event.add('summary', 'Stream: EmberCare - Medication Inventory UI')
event.add('dtstart', stream_start_utc)
event.add('dtend', stream_start_utc + timedelta(hours=4))
event.add('dtstamp', datetime.now(pytz.UTC))
event.add('uid', f'stream-20251104-embercare@macjunkins.com')
event.add('description', task_details)
event.add('location', 'Rumble')

# Add alarm (30 min before)
alarm = Alarm()
alarm.add('action', 'DISPLAY')
alarm.add('description', 'Stream starts in 30 minutes!')
alarm.add('trigger', timedelta(minutes=-30))
event.add_component(alarm)

cal.add_component(event)

# Write to file
with open('calendar.ics', 'wb') as f:
    f.write(cal.to_ical())
```

---

### Stream Plan Folder Structure

**Each generated folder contains:**

```
2025-11-04-1pm-epic-1/
├── stream-outline.md              # Hour-by-hour guide
├── pre-stream-checklist.md        # Pre-flight checklist
├── youtube-description.txt        # Copy-paste video description
└── social-media.txt               # Twitter + Discord posts
```

**Folder Naming Convention:**
```
{YYYY-MM-DD}-{TIME_SLUG}-{MILESTONE_SLUG}/

Examples:
- 2025-11-04-1pm-epic-1/
- 2025-11-06-1pm-phase-2-automation/
- 2025-11-08-1pm-yaml-conversion/
```

**Time Slug:**
- Always lowercase
- Remove colons and spaces
- Examples: `1pm`, `2pm`, `7pm`

**Milestone Slug:**
- Lowercase
- Replace spaces with hyphens
- Remove special characters
- Max 30 characters
- Examples:
  - "Epic 1: Medication Tracking" → `epic-1-medication-tracking`
  - "Phase 2 Automation" → `phase-2-automation`
  - "YAML Conversion (v2)" → `yaml-conversion-v2`

---

## Success Metrics

**Script is successful if:**
1. Generates valid markdown and ICS files without errors
2. Prioritization matches meta-roadmap strategic priorities
3. Stream schedule groups tasks logically by project
4. Time estimates total to 30 hours (6hr/day × 5 days)
5. Calendar import works in Google Calendar, Apple Calendar, Outlook
6. 5 stream plan folders generated automatically with all content ready
7. Social media content ready to schedule in advance

**User adoption signals:**
1. Used weekly for 4+ consecutive weeks
2. Reduces planning time from 2-3 hours to <30 minutes
3. Improves stream consistency (5-day/week cadence maintained)
4. Helps hit meta-roadmap quarterly milestones

---

## Future Enhancements (Post-MVP)

### v1.1 Features
- **Historical analysis**: Track actual time vs estimated time
- **Completion tracking**: Mark tasks as done, calculate velocity
- **Burndown charts**: Visualize progress toward quarterly goals
- **Slack/Discord integration**: Post stream schedule to channels

### v1.2 Features
- **AI suggestions**: Use Claude to suggest task priorities
- **Auto-issue creation**: Generate missing issues from roadmap
- **Stream analytics**: Track viewership by project/topic

### v2.0 Features
- **Web dashboard**: Interactive planning interface
- **Real-time updates**: Sync with GitHub webhooks
- **Team collaboration**: Multi-person planning support

---

## Open Questions

1. **Handling partially-completed tasks:**
   - Should the script detect if an issue is "in progress" and include it?
   - How to handle multi-week tasks?

2. **Dealing with interruptions/emergencies:**
   - Should there be "buffer time" built in?
   - How to adjust plan mid-week?

3. **Integration with other tools:**
   - Should it update GitHub project boards automatically?
   - Should it create calendar events for off-stream work too?

4. **Stream content decisions:**
   - Should it suggest stream titles automatically?
   - Should it avoid repeating the same project 3+ days in a row?

5. **Stream plan regeneration:**
   - Should regenerating overwrite existing folders or create versioned backups?
   - How to handle manually edited stream plans (don't overwrite)?
   - Should there be a --force flag for destructive overwrites?

---

## Performance Requirements

### Script Execution Time
- Target: Complete execution in under 2 minutes
- Acceptable: Up to 5 minutes for large portfolios (50+ open issues)
- GitHub API calls should be batched and cached when possible

### Output File Size
- Markdown plan: Typically 400-600 lines (~30KB)
- ICS calendar: Typically 200-300 lines (~15KB)
- Stream plan folders: 4 files × 5 folders = 20 files total

### Resource Usage
- Memory: Should run comfortably on systems with 4GB+ RAM
- Disk: Minimal (< 1MB total output per week)
- Network: Respectful of GitHub API rate limits (5000/hour authenticated)

---

## Security & Privacy

### GitHub Token Handling
- Reuse existing token from `portfolio_status.py`
- Never log or expose token in output
- Use environment variables or secure config

### Data Storage
- All generated files are local (no cloud storage)
- No PII collected or transmitted
- GitHub data cached locally for performance

### Safe Defaults
- Never commit generated plans to git automatically
- Never publish calendar events publicly
- Streaming folder paths remain private

---

## Maintainability

### Code Quality Standards
- Type hints on all function signatures
- Comprehensive docstrings (Google style)
- Unit test coverage > 80%
- Follow PEP 8 style guide

### Documentation
- Inline comments explain "why", not "what"
- README with quick start guide
- This spec as reference documentation
- Example outputs for validation

### Versioning
- Semantic versioning (v1.0.0, v1.1.0, etc.)
- Changelog maintained in CHANGELOG.md
- Backward compatibility for config files

---

## Estimated Implementation Impact

**Effort to implement stream planner integration:**
- Phase 3.5 (stream_planner.py): ~4-6 hours
- Update weekly_planner.py to call stream_planner: ~2 hours
- Refactor `/stream-plan` slash command to use shared library: ~2 hours
- Testing and validation: ~2 hours

**Total:** ~10-12 hours additional work on top of base weekly planner

**Value:** Eliminates 1-2 hours of manual stream planning work every Sunday + no need to run slash command before each stream (5 fewer manual steps per week)

---

## End of Non-Functional Requirements

**Ready for implementation:** 2025-11-02
**Estimated implementation time:** 3-5 days (base) + 1-2 days (stream integration)
**Owner:** John Junkins (@macjunkins)

---

**Questions or feedback?** Update this spec as design evolves.
