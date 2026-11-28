import os, tempfile, unittest
from core import add_task, complete_task
import stats

class TestStats(unittest.TestCase):
    def setUp(self):
        fd, self.db = tempfile.mkstemp(suffix=".json"); os.close(fd); os.unlink(self.db)
    def tearDown(self):
        if os.path.exists(self.db): os.unlink(self.db)
    def test_stats_counts(self):
        add_task(self.db, "a"); tid = add_task(self.db, "b"); add_task(self.db, "c")
        complete_task(self.db, tid)
        self.assertEqual(stats.stats(self.db), {"total": 3, "done": 1, "open": 2})
    def test_stats_empty(self):
        self.assertEqual(stats.stats(self.db), {"total": 0, "done": 0, "open": 0})

if __name__ == "__main__":
    unittest.main()
