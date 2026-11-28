import os, sqlite3, tempfile, unittest
from migrate import migrate, SCHEMA_VERSION

def make_v1(path):
    conn = sqlite3.connect(path)
    conn.execute("CREATE TABLE tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL, done INTEGER NOT NULL DEFAULT 0)")
    conn.executemany("INSERT INTO tasks (title, done) VALUES (?, ?)", [("a", 0), ("b", 1), ("c", 0)])
    conn.commit(); conn.close()

class TestMigration(unittest.TestCase):
    def setUp(self):
        fd, self.db = tempfile.mkstemp(suffix=".db"); os.close(fd); os.unlink(self.db)
    def tearDown(self):
        if os.path.exists(self.db): os.unlink(self.db)
    def test_migrate_v1_preserves_rows_and_backfills(self):
        make_v1(self.db); migrate(self.db)
        conn = sqlite3.connect(self.db)
        rows = conn.execute("SELECT title, done, priority FROM tasks ORDER BY id").fetchall()
        self.assertEqual(rows, [("a", 0, 2), ("b", 1, 2), ("c", 0, 2)])
    def test_migrate_records_schema_version(self):
        make_v1(self.db); migrate(self.db)
        conn = sqlite3.connect(self.db)
        v = conn.execute("SELECT version FROM schema_version").fetchone()[0]
        self.assertEqual(v, SCHEMA_VERSION)
    def test_migrate_idempotent(self):
        make_v1(self.db); migrate(self.db); migrate(self.db)
        conn = sqlite3.connect(self.db)
        self.assertEqual(conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0], 3)
        self.assertEqual(conn.execute("SELECT COUNT(*) FROM schema_version").fetchone()[0], 1)
    def test_migrate_fresh_db_creates_full_schema(self):
        migrate(self.db)
        conn = sqlite3.connect(self.db)
        conn.execute("INSERT INTO tasks (title, done, priority) VALUES ('x', 0, 1)")
        self.assertEqual(conn.execute("SELECT priority FROM tasks").fetchone()[0], 1)
    def test_app_add_task_uses_priority(self):
        migrate(self.db)
        import app
        conn = app.connect(self.db)
        app.add_task(conn, "hi", priority=1)
        self.assertEqual(conn.execute("SELECT priority FROM tasks WHERE title='hi'").fetchone()[0], 1)
        app.add_task(conn, "default")
        self.assertEqual(conn.execute("SELECT priority FROM tasks WHERE title='default'").fetchone()[0], 2)

if __name__ == "__main__":
    unittest.main()
