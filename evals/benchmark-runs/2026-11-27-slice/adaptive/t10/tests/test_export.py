import json, os, tempfile, unittest
from core import add_task, complete_task
import export

class TestExport(unittest.TestCase):
    def setUp(self):
        fd, self.db = tempfile.mkstemp(suffix=".json"); os.close(fd); os.unlink(self.db)
        add_task(self.db, "a"); tid = add_task(self.db, "b"); complete_task(self.db, tid)
    def tearDown(self):
        if os.path.exists(self.db): os.unlink(self.db)
    def test_export_json(self):
        data = json.loads(export.export_tasks(self.db, "json"))
        self.assertEqual([t["title"] for t in data], ["a", "b"])
        self.assertTrue(data[1]["done"])
    def test_export_csv(self):
        lines = export.export_tasks(self.db, "csv").splitlines()
        self.assertEqual(lines[0], "id,title,done")
        self.assertEqual(lines[1], "1,a,False")
        self.assertEqual(lines[2], "2,b,True")
    def test_export_bad_format(self):
        with self.assertRaises(ValueError):
            export.export_tasks(self.db, "xml")

if __name__ == "__main__":
    unittest.main()
