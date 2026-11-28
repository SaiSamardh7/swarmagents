# Assumptions — "People keep missing overdue work"

## Questions I would ask the user

1. Should overdue be about **due dates** (tasks have deadlines) or **staleness** (tasks untouched too long)? These are different features.
2. Where should overdue work surface — a filter the user asks for (`list --overdue`), a warning on every `list`, or both?
3. Should a completed task ever count as overdue (e.g., for reporting), or only open tasks?
4. Is "due today" overdue, or does overdue start the day after?

## Assumptions recorded (no user available in this benchmark)

- Overdue means **past an explicit due date**: deadlines are the common reading of "overdue", and staleness detection can be layered on later.
- Due dates are **optional** on `add` (`--due YYYY-MM-DD`); existing tasks and workflows are untouched.
- Overdue surfaces as an explicit filter (`list --overdue`) rather than noisy warnings on every command.
- Only **open** tasks can be overdue; a done task is done.
- **Due today is not overdue** — overdue begins the day after the deadline.
- Dates compare as ISO-8601 strings/dates in local time; no time-of-day precision.

These match the reference interpretation encoded in `tests/test_overdue.py`.
