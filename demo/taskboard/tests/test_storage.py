import json
import os
import sys
import tempfile
import threading
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from storage import TaskStore  # noqa: E402


class TaskStoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = os.path.join(self.tmp.name, "tasks.json")
        self.store = TaskStore(self.path)

    def test_empty_on_missing_file(self):
        self.assertEqual(self.store.list_tasks(), [])

    def test_add_strips_and_returns_task(self):
        t = self.store.add_task("  hello  ")
        self.assertEqual(t["title"], "hello")
        self.assertIs(t["done"], False)
        self.assertTrue(t["id"])
        self.assertTrue(t["created_at"])

    def test_add_empty_or_whitespace_raises(self):
        for bad in ("", "   ", None, 5):
            with self.assertRaises(ValueError):
                self.store.add_task(bad)

    def test_add_title_length_limit(self):
        self.assertEqual(len(self.store.add_task("x" * 200)["title"]), 200)
        with self.assertRaises(ValueError):
            self.store.add_task("x" * 201)

    def test_newest_first(self):
        for n in ("a", "b", "c"):
            self.store.add_task(n)
        self.assertEqual([t["title"] for t in self.store.list_tasks()], ["c", "b", "a"])

    def test_update_task(self):
        t = self.store.add_task("a")
        u = self.store.update_task(t["id"], True)
        self.assertIs(u["done"], True)
        self.assertIs(self.store.list_tasks()[0]["done"], True)
        self.assertIs(self.store.update_task(t["id"], False)["done"], False)

    def test_update_unknown_keyerror(self):
        with self.assertRaises(KeyError):
            self.store.update_task("nope", True)

    def test_delete_task(self):
        a = self.store.add_task("a")
        b = self.store.add_task("b")
        self.store.delete_task(a["id"])
        self.assertEqual([t["id"] for t in self.store.list_tasks()], [b["id"]])

    def test_delete_unknown_keyerror(self):
        with self.assertRaises(KeyError):
            self.store.delete_task("nope")

    def test_persistence_across_instances(self):
        t = self.store.add_task("keep me")
        self.store.update_task(t["id"], True)
        other = TaskStore(self.path)
        tasks = other.list_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["title"], "keep me")
        self.assertIs(tasks[0]["done"], True)

    def test_corrupt_json_raises_valueerror(self):
        with open(self.path, "w") as f:
            f.write("{not json")
        with self.assertRaises(ValueError):
            self.store.list_tasks()

    def test_non_list_json_raises_valueerror(self):
        with open(self.path, "w") as f:
            json.dump({"a": 1}, f)
        with self.assertRaises(ValueError):
            self.store.list_tasks()

    def test_no_leftover_tmp_files(self):
        self.store.add_task("a")
        self.assertEqual(os.listdir(self.tmp.name), ["tasks.json"])

    def test_concurrent_adds(self):
        errors = []

        def work(i):
            try:
                for j in range(5):
                    self.store.add_task("t%d-%d" % (i, j))
            except Exception as e:  # pragma: no cover
                errors.append(e)

        threads = [threading.Thread(target=work, args=(i,)) for i in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        self.assertEqual(errors, [])
        tasks = self.store.list_tasks()
        self.assertEqual(len(tasks), 40)
        self.assertEqual(len({t["id"] for t in tasks}), 40)


if __name__ == "__main__":
    unittest.main()
