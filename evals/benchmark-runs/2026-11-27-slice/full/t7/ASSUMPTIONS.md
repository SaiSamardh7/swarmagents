# Assumptions and Clarifying Questions

Request: "People keep missing overdue work in taskman. Do something about it."

## Clarifying questions I would ask
1. Who are "people" (solo CLI users, a team sharing one tasks.json)? Is there any notion of users or assignees?
2. Do tasks have due dates today? (No: the schema is id/title/done.) Should due dates be optional or required?
3. What does "missing" mean: not noticing, forgetting, or not seeing in the list output? Passive visibility or active notification?
4. Is a task due today overdue, or only after the day ends?
5. Are notifications (email, desktop, cron reminders) in scope, or only in-CLI surfacing?
6. Date format and timezone? Time-of-day granularity?
7. Should existing tasks without due dates be migrated or ever flagged?
8. Should done tasks ever appear as overdue? Should overdue tasks be visually marked in the normal `list`?
9. Is recurring/snooze/priority in scope?

## Assumptions chosen
- A1: Single local user, JSON file store; no users, assignees, or notifications.
- A2: "Missing overdue work" is solved by making overdue work queryable and visible in the CLI, not by pushing notifications.
- A3: Due date is optional, stored as an ISO `YYYY-MM-DD` string under key `due`; no time-of-day, no timezone (date-local).
- A4: Overdue = not done AND has a due date AND due < today. A task due today is NOT overdue.
- A5: Tasks without a due date are never overdue. Done tasks are never overdue.
- A6: Legacy tasks (no `due` key) remain valid; no migration. Tasks added without `--due` do not get a `due` key forced to a value (None/absent both treated as no due date).
- A7: `list_overdue(path, today=None)` takes an injectable `today` (datetime.date) for testability; defaults to `date.today()`.
- A8: CLI: `add TITLE --due YYYY-MM-DD` (validated, invalid dates rejected with an error) and `list --overdue` (filters to overdue tasks). Plain `list` output stays backward-compatible.
- A9: Out of scope: reminders, recurrence, priorities, snooze, editing due dates after creation.
