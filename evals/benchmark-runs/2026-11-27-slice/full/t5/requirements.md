# Requirements: Schema v2 Migration (t5)

## Context
`app.py` is a v1 sqlite task app: `tasks(id, title, done)`. Ship schema v2 via a new `migrate.py` and a small `app.add_task` update. `tests/` is read-only and is the spec.

## Requirements

### R1 Module surface
- `migrate.py` at repo root (importable as `from migrate import migrate, SCHEMA_VERSION`).
- `SCHEMA_VERSION` is an integer constant, value 2.
- `migrate(db_path)` opens/creates the sqlite file at `db_path`, migrates it, commits, and closes its connection.

### R2 Backfill (v1 -> v2)
- Add `priority INTEGER NOT NULL DEFAULT 2` to `tasks`.
- All existing rows keep `id`, `title`, `done` unchanged and receive `priority = 2`.
- No row loss, reordering, or id change.

### R3 Versioning
- Create table `schema_version` with a `version` column (tests read `SELECT version FROM schema_version`).
- After migration it holds exactly one row, `version == SCHEMA_VERSION`.

### R4 Idempotency
- Running `migrate` repeatedly must not error (no duplicate-column failure), must not duplicate or alter task rows, and must leave exactly one `schema_version` row.
- Detect existing state (e.g. check `PRAGMA table_info(tasks)` for `priority`; update or insert-if-absent the version row) rather than blindly altering.

### R5 Fresh/empty database
- If `db_path` does not exist or has no `tasks` table, create the full v2 `tasks` table (`id INTEGER PRIMARY KEY, title TEXT NOT NULL, done INTEGER NOT NULL DEFAULT 0, priority INTEGER NOT NULL DEFAULT 2`) plus `schema_version` recording `SCHEMA_VERSION`.
- Inserting `(title, done, priority)` must work afterwards.

### R6 App change
- `app.add_task(conn, title, priority=2)` inserts `priority` with the row; default is 2; commits.
- `list_tasks` signature/behavior unchanged (not covered by tests; do not break it).

### R7 Constraints
- Do not modify `tests/`. Standard library only.
- Suite command: `python3 -m unittest discover -s tests -t .`

## Acceptance Criteria

| ID | Criterion | Test |
|----|-----------|------|
| AC1 | Migrating a v1 DB with rows a/b/c preserves title and done and sets priority 2 on every row, in id order | `test_migrate_v1_preserves_rows_and_backfills` |
| AC2 | After migrate, `schema_version.version` equals `SCHEMA_VERSION` | `test_migrate_records_schema_version` |
| AC3 | Calling migrate twice keeps task count at 3 | `test_migrate_idempotent` |
| AC4 | Calling migrate twice leaves exactly 1 `schema_version` row | `test_migrate_idempotent` |
| AC5 | Migrate on a nonexistent/empty DB creates full v2 schema; insert with `priority` works and reads back 1 | `test_migrate_fresh_db_creates_full_schema` |
| AC6 | `add_task(conn, "hi", priority=1)` stores priority 1 | `test_app_add_task_uses_priority` |
| AC7 | `add_task(conn, "default")` stores priority 2 | `test_app_add_task_uses_priority` |
| AC8 | `migrate` and `SCHEMA_VERSION` import cleanly from `migrate` (module-level import in the test file) | all tests (import) |
| AC9 | Full suite passes via the unittest discover command with `tests/` unmodified | whole suite |

## Notes / Risks
- Fresh-db case: migrating a nonexistent path makes sqlite create the file; tests unlink it in tearDown only if it exists.
- `ALTER TABLE ADD COLUMN ... NOT NULL DEFAULT 2` backfills existing rows automatically in sqlite; an explicit `UPDATE` is unnecessary but harmless.
- Closing connections matters so tearDown can unlink the file.
