import os, tempfile, unittest
from core import add_task, complete_task, list_tasks

class TestCore(unittest.TestCase):
    def setUp(self):
        fd, self.db = tempfile.mkstemp(suffix=".json"); os.close(fd); os.unlink(self.db)
    def tearDown(self):
        if os.path.exists(self.db): os.unlink(self.db)
    def test_add_and_list(self):
        add_task(self.db, "a"); add_task(self.db, "b")
        self.assertEqual([t["title"] for t in list_tasks(self.db)], ["a", "b"])
    def test_complete(self):
        tid = add_task(self.db, "a")
        self.assertTrue(complete_task(self.db, tid))
        self.assertTrue(list_tasks(self.db)[0]["done"])
    def test_complete_missing(self):
        self.assertFalse(complete_task(self.db, 99))

if __name__ == "__main__":
    unittest.main()
