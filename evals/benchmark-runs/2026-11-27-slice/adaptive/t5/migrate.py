import sqlite3

SCHEMA_VERSION = 2


def migrate(db_path):
    conn = sqlite3.connect(db_path, isolation_level=None)
    try:
        conn.execute("BEGIN IMMEDIATE")
        try:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS schema_version ("
                "id INTEGER PRIMARY KEY CHECK (id = 1), version INTEGER NOT NULL)"
            )
            row = conn.execute("SELECT version FROM schema_version WHERE id = 1").fetchone()
            current = row[0] if row else None
            if current is not None and current > SCHEMA_VERSION:
                raise RuntimeError(
                    f"database schema version {current} is newer than supported {SCHEMA_VERSION}"
                )
            if current != SCHEMA_VERSION:
                conn.execute(
                    "CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, "
                    "title TEXT NOT NULL, done INTEGER NOT NULL DEFAULT 0, "
                    "priority INTEGER NOT NULL DEFAULT 2)"
                )
                cols = [r[1] for r in conn.execute("PRAGMA table_info(tasks)")]
                if "priority" not in cols:
                    conn.execute(
                        "ALTER TABLE tasks ADD COLUMN priority INTEGER NOT NULL DEFAULT 2"
                    )
                conn.execute(
                    "INSERT OR REPLACE INTO schema_version (id, version) VALUES (1, ?)",
                    (SCHEMA_VERSION,),
                )
            conn.execute("COMMIT")
        except BaseException:
            conn.execute("ROLLBACK")
            raise
    finally:
        conn.close()
