# Requirements: Overdue task surfacing in taskman

Tests: `tests/test_overdue.py` (class TestOverdue). Existing `tests/test_base.py` must keep passing.

## Functional requirements
- R1: `add_task(path, title, due=None)` accepts an optional due date (ISO `YYYY-MM-DD`) and persists it as `due`.
- R2: `add_task` without `due` behaves exactly as before and returns the new id.
- R3: `list_overdue(path, today=None)` returns tasks that are not done, have a due date, and due < today. `today` defaults to `date.today()`.
- R4: CLI `add TITLE --due YYYY-MM-DD` passes the date to `add_task`; invalid format yields a non-zero exit with an error message.
- R5: CLI `list --overdue` prints only overdue tasks, in the same line format as `list`.
- R6: Plain `list` and legacy tasks without `due` remain unchanged and valid.

## Acceptance criteria
| ID | Criterion | Test |
|----|-----------|------|
| AC1 | Adding with `due="2026-01-15"` stores `due == "2026-01-15"` in the persisted task | `test_add_with_due_persists` |
| AC2 | Adding without `due` works and the task is persisted | `test_add_without_due_still_works` |
| AC3 | With today=2026-06-01, only the past-due open task is returned; future-due and no-due tasks are excluded | `test_list_overdue_returns_past_due_open_tasks` |
| AC4 | A past-due task marked done is excluded from overdue results | `test_list_overdue_excludes_done` |
| AC5 | A task due on `today` is not overdue (strictly before) | `test_due_today_is_not_overdue` |
| AC6 | CLI `add --due` and `list --overdue` work; invalid date rejected (not covered by test file; manual verification) | manual |
| AC7 | `tests/test_base.py` still passes (no regression) | `test_base.py` |
