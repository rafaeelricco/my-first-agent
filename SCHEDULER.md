# Scheduled Agent Execution

This project uses [APScheduler 4](https://github.com/agronholm/apscheduler) to run the agent on a configurable schedule.

## Configuration

| Environment Variable | Type | Default | Description |
|---------------------|------|---------|-------------|
| `SCHEDULE_INTERVAL_MINUTES` | `int` | `60` | Interval between runs (minutes) |
| `SCHEDULE_CRON` | `str \| None` | `None` | Cron expression (overrides interval) |

## Usage

### Interval-based scheduling

```bash
# Run every 30 minutes
export SCHEDULE_INTERVAL_MINUTES=30
.venv/bin/python main.py
```

### Cron-based scheduling

```bash
# Run every 15 minutes during business hours (Mon-Fri, 9am-5pm)
export SCHEDULE_CRON="*/15 9-17 * * mon-fri"
.venv/bin/python main.py
```

## Cron Expression Format

```
┌───────────── minute (0-59)
│ ┌───────────── hour (0-23)
│ │ ┌───────────── day of month (1-31)
│ │ │ ┌───────────── month (1-12)
│ │ │ │ ┌───────────── day of week (mon-sun)
│ │ │ │ │
* * * * *
```

### Examples

| Expression | Description |
|-----------|-------------|
| `0 * * * *` | Every hour at minute 0 |
| `*/15 * * * *` | Every 15 minutes |
| `0 9 * * *` | Daily at 9:00 AM |
| `0 9 * * mon-fri` | Weekdays at 9:00 AM |
| `0 9,18 * * *` | Daily at 9:00 AM and 6:00 PM |
| `*/30 8-18 * * mon-fri` | Every 30 min, 8am-6pm, Mon-Fri |

## Architecture

```
main.py
├── create_trigger(cfg) -> IntervalTrigger | CronTrigger
├── create_agent(cfg) -> Agent
├── run_agent_task() -> None
└── main() -> scheduler loop
```

- **Pure functions**: `create_trigger` and `create_agent` are side-effect free
- **Type-safe**: Full type annotations with union types
- **Graceful shutdown**: `Ctrl+C` stops the scheduler cleanly
