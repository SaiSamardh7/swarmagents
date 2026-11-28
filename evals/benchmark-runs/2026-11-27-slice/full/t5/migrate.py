import sqlite3

SCHEMA_VERSION = 2


def migrate(db_path):
    conn = sqlite3.connect(db_path, isolation_level=None)
    try:
        conn.execute("BEGIN IMMEDIATE")
        try:
            has_sv = conn.execute(
                "SELECT 1 FROM sqlite_master WHERE type='table' AND name='schema_version'"
            ).fetchone()
            current = None
            if has_sv:
                cols = [r[1] for r in conn.execute("PRAGMA table_info(schema_version)")]
                if "version" in cols:
                    row = conn.execute("SELECT MAX(version) FROM schema_version").fetchone()
                    current = row[0] if row else None
            if current is not None:
                if current > SCHEMA_VERSION:
                    raise RuntimeError(
                        f"database schema_version {current} is newer than supported {SCHEMA_VERSION}"
                    )
                if current == SCHEMA_VERSION and "id" in cols:
                    conn.execute("COMMIT")
                    return
            conn.execute(
                "CREATE TABLE IF NOT EXISTS tasks ("
                "id INTEGER PRIMARY KEY, title TEXT NOT NULL, "
                "done INTEGER NOT NULL DEFAULT 0, "
                "priority INTEGER NOT NULL DEFAULT 2)"
            )
            tcols = [r[1] for r in conn.execute("PRAGMA table_info(tasks)")]
            if "priority" not in tcols:
                conn.execute(
                    "ALTER TABLE tasks ADD COLUMN priority INTEGER NOT NULL DEFAULT 2"
                )
            # single-row table; rebuild legacy multi-row/no-id layout
            conn.execute("DROP TABLE IF EXISTS schema_version")
            conn.execute(
                "CREATE TABLE schema_version ("
                "id INTEGER PRIMARY KEY CHECK(id=1), version INTEGER NOT NULL)"
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
