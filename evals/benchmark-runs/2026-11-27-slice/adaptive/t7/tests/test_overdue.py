import os, tempfile, unittest
from datetime import date
from core import add_task, complete_task, list_overdue
from storage import load_tasks

class TestOverdue(unittest.TestCase):
    def setUp(self):
        fd, self.db = tempfile.mkstemp(suffix=".json"); os.close(fd); os.unlink(self.db)
    def tearDown(self):
        if os.path.exists(self.db): os.unlink(self.db)
    def test_add_with_due_persists(self):
        add_task(self.db, "a", due="2026-01-15")
        self.assertEqual(load_tasks(self.db)[0]["due"], "2026-01-15")
    def test_add_without_due_still_works(self):
        add_task(self.db, "a")
        self.assertEqual(len(load_tasks(self.db)), 1)
    def test_list_overdue_returns_past_due_open_tasks(self):
        add_task(self.db, "late", due="2026-01-15")
        add_task(self.db, "future", due="2026-12-31")
        add_task(self.db, "no-due")
        over = list_overdue(self.db, today=date(2026, 6, 1))
        self.assertEqual([t["title"] for t in over], ["late"])
    def test_list_overdue_excludes_done(self):
        tid = add_task(self.db, "late-done", due="2026-01-15")
        complete_task(self.db, tid)
        self.assertEqual(list_overdue(self.db, today=date(2026, 6, 1)), [])
    def test_due_today_is_not_overdue(self):
        add_task(self.db, "today", due="2026-06-01")
        self.assertEqual(list_overdue(self.db, today=date(2026, 6, 1)), [])

if __name__ == "__main__":
    unittest.main()
