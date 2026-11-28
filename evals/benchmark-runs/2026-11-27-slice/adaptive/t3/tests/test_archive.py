import io, os, tempfile, unittest
from contextlib import redirect_stdout
from core import add_task, archive_task, list_tasks
import cli
from storage import load_tasks, save_tasks

class TestArchive(unittest.TestCase):
    def setUp(self):
        fd, self.db = tempfile.mkstemp(suffix=".json"); os.close(fd); os.unlink(self.db)
    def tearDown(self):
        if os.path.exists(self.db): os.unlink(self.db)
    def test_archive_marks_and_persists(self):
        tid = add_task(self.db, "a")
        self.assertTrue(archive_task(self.db, tid))
        raw = load_tasks(self.db)
        self.assertTrue(raw[0]["archived"])
    def test_archive_missing_returns_false(self):
        self.assertFalse(archive_task(self.db, 99))
    def test_list_excludes_archived_by_default(self):
        a = add_task(self.db, "a"); add_task(self.db, "b")
        archive_task(self.db, a)
        self.assertEqual([t["title"] for t in list_tasks(self.db)], ["b"])
    def test_list_include_archived(self):
        a = add_task(self.db, "a"); add_task(self.db, "b")
        archive_task(self.db, a)
        titles = [t["title"] for t in list_tasks(self.db, include_archived=True)]
        self.assertEqual(sorted(titles), ["a", "b"])
    def test_legacy_file_without_archived_field_loads(self):
        save_tasks(self.db, [{"id": 1, "title": "old", "done": False}])
        self.assertEqual([t["title"] for t in list_tasks(self.db)], ["old"])
        self.assertTrue(archive_task(self.db, 1))
        self.assertEqual(list_tasks(self.db), [])
    def test_cli_archive_and_list_flag(self):
        tid = add_task(self.db, "a"); add_task(self.db, "b")
        out = io.StringIO()
        with redirect_stdout(out):
            cli.main(["--db", self.db, "archive", str(tid)])
            cli.main(["--db", self.db, "list"])
        self.assertNotIn("a", [l.split()[-1] for l in out.getvalue().splitlines() if l.startswith("[")])
        out2 = io.StringIO()
        with redirect_stdout(out2):
            cli.main(["--db", self.db, "list", "--archived"])
        names = [l.split()[-1] for l in out2.getvalue().splitlines() if l.startswith("[")]
        self.assertIn("a", names); self.assertIn("b", names)

if __name__ == "__main__":
    unittest.main()
