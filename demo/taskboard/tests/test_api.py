import json
import os
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from server import create_server  # noqa: E402


class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.data_path = os.path.join(self.tmp.name, "tasks.json")
        self.servers = []
        self.start()

    def start(self):
        server = create_server(0, self.data_path)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.servers.append((server, thread))
        self.server = server
        self.base = "http://127.0.0.1:%d" % server.server_address[1]

    def stop(self):
        server, thread = self.servers.pop()
        server.shutdown()
        server.server_close()
        thread.join(5)

    def tearDown(self):
        while self.servers:
            self.stop()

    def req(self, method, path, body=None, raw=None):
        data = raw if raw is not None else (
            None if body is None else json.dumps(body).encode())
        r = urllib.request.Request(self.base + path, data=data, method=method)
        if data is not None:
            r.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(r) as resp:
                return resp.status, resp.headers, resp.read()
        except urllib.error.HTTPError as e:
            return e.code, e.headers, e.read()

    def jreq(self, method, path, body=None, raw=None):
        status, headers, data = self.req(method, path, body, raw)
        return status, (json.loads(data) if data else None)

    def add(self, title):
        status, body = self.jreq("POST", "/api/tasks", {"title": title})
        self.assertEqual(status, 201)
        return body["task"]


class TaskApiTests(ApiTestCase):
    def test_list_empty(self):
        self.assertEqual(self.jreq("GET", "/api/tasks"), (200, {"tasks": []}))

    def test_create_returns_201_task(self):
        status, body = self.jreq("POST", "/api/tasks", {"title": "  Buy milk "})
        self.assertEqual(status, 201)
        t = body["task"]
        self.assertEqual(t["title"], "Buy milk")
        self.assertIs(t["done"], False)
        self.assertIn("id", t)
        self.assertIn("created_at", t)

    def test_create_invalid_titles_400(self):
        for body in ({}, {"title": ""}, {"title": "   "}, {"title": "x" * 201},
                     {"title": 5}, {"title": None}):
            status, resp = self.jreq("POST", "/api/tasks", body)
            self.assertEqual(status, 400, body)
            self.assertIn("error", resp)

    def test_create_max_length_ok(self):
        self.add("x" * 200)

    def test_create_invalid_json_400(self):
        for raw in (b"{not json", b"", b"[1,2]", b'"str"'):
            status, resp = self.jreq("POST", "/api/tasks", raw=raw)
            self.assertEqual(status, 400, raw)
            self.assertIn("error", resp)

    def test_list_newest_first(self):
        for n in ("a", "b", "c"):
            self.add(n)
        _, body = self.jreq("GET", "/api/tasks")
        self.assertEqual([t["title"] for t in body["tasks"]], ["c", "b", "a"])

    def test_patch_done_toggle(self):
        t = self.add("a")
        status, body = self.jreq("PATCH", "/api/tasks/" + t["id"], {"done": True})
        self.assertEqual(status, 200)
        self.assertIs(body["task"]["done"], True)
        _, lst = self.jreq("GET", "/api/tasks")
        self.assertIs(lst["tasks"][0]["done"], True)
        status, body = self.jreq("PATCH", "/api/tasks/" + t["id"], {"done": False})
        self.assertEqual(status, 200)
        self.assertIs(body["task"]["done"], False)

    def test_patch_invalid_body_400(self):
        t = self.add("a")
        for body in ({"done": "yes"}, {"done": 1}, {"done": None}, {}, {"title": "x"}):
            status, resp = self.jreq("PATCH", "/api/tasks/" + t["id"], body)
            self.assertEqual(status, 400, body)
            self.assertIn("error", resp)
        status, _ = self.jreq("PATCH", "/api/tasks/" + t["id"], raw=b"garbage")
        self.assertEqual(status, 400)

    def test_patch_unknown_404(self):
        status, resp = self.jreq("PATCH", "/api/tasks/nope", {"done": True})
        self.assertEqual(status, 404)
        self.assertIn("error", resp)

    def test_delete(self):
        t = self.add("a")
        status, _, data = self.req("DELETE", "/api/tasks/" + t["id"])
        self.assertEqual(status, 204)
        self.assertEqual(data, b"")
        self.assertEqual(self.jreq("GET", "/api/tasks")[1], {"tasks": []})

    def test_delete_unknown_404(self):
        status, resp = self.jreq("DELETE", "/api/tasks/nope")
        self.assertEqual(status, 404)
        self.assertIn("error", resp)

    def test_delete_twice_404(self):
        t = self.add("a")
        self.assertEqual(self.req("DELETE", "/api/tasks/" + t["id"])[0], 204)
        self.assertEqual(self.req("DELETE", "/api/tasks/" + t["id"])[0], 404)

    def test_persistence_across_server_restart(self):
        a = self.add("first")
        b = self.add("second")
        self.jreq("PATCH", "/api/tasks/" + a["id"], {"done": True})
        self.stop()
        self.start()
        _, body = self.jreq("GET", "/api/tasks")
        self.assertEqual([t["title"] for t in body["tasks"]], ["second", "first"])
        self.assertEqual([t["done"] for t in body["tasks"]], [False, True])
        self.assertEqual(body["tasks"][0]["id"], b["id"])


class StaticTests(ApiTestCase):
    def test_index(self):
        for path in ("/", "/index.html"):
            status, headers, data = self.req("GET", path)
            self.assertEqual(status, 200)
            self.assertTrue(headers["Content-Type"].startswith("text/html"))
            self.assertIn(b"<html", data.lower())

    def test_css_and_js(self):
        status, headers, data = self.req("GET", "/style.css")
        self.assertEqual(status, 200)
        self.assertIn("css", headers["Content-Type"])
        self.assertTrue(data)
        status, headers, data = self.req("GET", "/app.js")
        self.assertEqual(status, 200)
        self.assertIn("javascript", headers["Content-Type"])
        self.assertTrue(data)

    def test_missing_static_404(self):
        self.assertEqual(self.req("GET", "/nope.txt")[0], 404)

    def test_path_traversal_404(self):
        import socket
        port = self.server.server_address[1]
        for path in ("/../server.py", "/%2e%2e/server.py", "/../storage.py",
                     "/%2e%2e/%2e%2e/etc/passwd"):
            # raw socket so the client does not normalise the path
            with socket.create_connection(("127.0.0.1", port), timeout=5) as s:
                s.sendall(("GET %s HTTP/1.0\r\nHost: x\r\n\r\n" % path).encode())
                resp = b""
                while True:
                    chunk = s.recv(4096)
                    if not chunk:
                        break
                    resp += chunk
            self.assertTrue(resp.startswith(b"HTTP/1.0 404") or resp.startswith(b"HTTP/1.1 404"),
                            (path, resp[:80]))
            self.assertNotIn(b"create_server", resp, path)


if __name__ == "__main__":
    unittest.main()
