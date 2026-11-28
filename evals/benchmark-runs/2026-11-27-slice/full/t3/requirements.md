# Requirements: Archive Tasks (taskman)

## Feature summary
Add an archive feature to taskman across storage, core and CLI. Tasks carry an `archived` boolean (default false). Archived tasks are hidden from listings by default and shown on request. Legacy data files without the field must keep working.

## Current state
- storage.py: `load_tasks`/`save_tasks` read/write a JSON list verbatim (no schema).
- core.py: `add_task` creates `{id,title,done}`; `complete_task`; `list_tasks(path)` returns all tasks.
- cli.py: subcommands `add`, `done`, `list`; global `--db`.

## Layer requirements

### Storage (storage.py)
- S1. Tasks persist an `archived` field (bool, default false).
- S2. Files lacking `archived` on a task must load without error; missing field is treated as false (either defaulted on load or tolerated via `.get("archived", False)` by consumers).
- S3. Round-trip: a saved `archived: true` value is returned by `load_tasks`.

### Core (core.py)
- C1. `archive_task(path, task_id)` sets `archived = True` on the matching task, persists, returns `True`.
- C2. `archive_task` returns `False` when no task has the id (including nonexistent file) and writes nothing harmful.
- C3. `list_tasks(path)` excludes archived tasks by default.
- C4. `list_tasks(path, include_archived=True)` returns all tasks, archived included.
- C5. `add_task` should create new tasks with `archived: False`.
- C6. Legacy tasks (no `archived` key) count as not archived in `list_tasks` and are archivable by `archive_task`.
- C7. Existing behaviour (`add_task`, `complete_task`, ids) unchanged; tests/test_core.py must still pass.

### CLI (cli.py)
- L1. New subcommand `archive <id>` (int id) calls `archive_task`; prints `ok` on success, `not found` otherwise (consistent with `done`).
- L2. `list` excludes archived tasks by default.
- L3. `list --archived` includes archived tasks; output format unchanged (`[x| ] id title`).

## Acceptance criteria

| ID | Criterion | Test (tests/test_archive.py) |
|----|-----------|------------------------------|
| AC1 | Archiving an existing task returns True and persists `archived == True` in the stored data | test_archive_marks_and_persists |
| AC2 | Archiving a nonexistent id returns False | test_archive_missing_returns_false |
| AC3 | Default `list_tasks` omits archived tasks | test_list_excludes_archived_by_default |
| AC4 | `list_tasks(..., include_archived=True)` returns archived and non-archived tasks | test_list_include_archived |
| AC5 | A legacy file lacking `archived` loads, lists as unarchived, can be archived, and is then hidden from default list | test_legacy_file_without_archived_field_loads |
| AC6 | CLI `archive <id>` archives; `list` hides it; `list --archived` shows all tasks | test_cli_archive_and_list_flag |

Also: full suite `python3 -m unittest discover -s tests` passes, with no test file modified (regression guard, covers C7 via tests/test_core.py).

## Notes
- Test imports `core` and `cli` as top-level modules, so tests run from the t3 directory.
- Unmapped by tests: C5 and the exact CLI `archive` output text (L1); both are recommended, not test-enforced.
