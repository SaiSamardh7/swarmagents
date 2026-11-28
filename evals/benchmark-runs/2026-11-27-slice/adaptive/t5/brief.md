# Task 5: Database migration

`app.py` is a v1 sqlite task app: table `tasks(id, title, done)`. Ship schema v2:

- Write `migrate.py` exposing `migrate(db_path)` and a `SCHEMA_VERSION` constant:
  adds column `priority INTEGER NOT NULL DEFAULT 2` backfilled to 2 for existing
  rows, creates a `schema_version` table recording `SCHEMA_VERSION`, is idempotent
  (safe to run twice), and on a fresh/empty database creates the full v2 schema.
- Update `app.add_task(conn, title, priority=2)` to store the priority.

`tests/test_migration.py` specifies the behavior and currently fails. Make the suite
pass (`python3 -m unittest discover -s tests -t .`) without modifying tests/.
