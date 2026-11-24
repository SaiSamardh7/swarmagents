"""Taskboard HTTP server: JSON API under /api/tasks plus static files."""
import argparse
import json
import mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from storage import StorageError, TaskStore

MAX_BODY = 64 * 1024
STATIC_DIR = (Path(__file__).resolve().parent / "static").resolve()
TYPES = {".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8",
         ".js": "application/javascript; charset=utf-8"}


class Handler(BaseHTTPRequestHandler):
    store = None  # set by create_server

    # ---- helpers ----
    def _send(self, status, payload=None):
        body = b"" if payload is None else json.dumps(payload).encode("utf-8")
        self.send_response(status)
        if payload is not None:
            self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if body:
            self.wfile.write(body)

    def _error(self, status, message, allow=None):
        body = json.dumps({"error": message}).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        if allow:
            self.send_header("Allow", allow)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        """Return parsed JSON object, or None if the body is invalid or too large."""
        try:
            length = int(self.headers.get("Content-Length") or 0)
            if not 0 <= length <= MAX_BODY:
                return None
            data = json.loads(self.rfile.read(length).decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            return None
        return data if isinstance(data, dict) else None

    def _task_id(self):
        """Return the id for /api/tasks/{id}, or None for other paths."""
        parts = self.path.split("?", 1)[0].split("/")
        if len(parts) == 4 and parts[:3] == ["", "api", "tasks"] and parts[3]:
            return parts[3]
        return None

    def _is_collection(self):
        return self.path.split("?", 1)[0].rstrip("/") == "/api/tasks"

    def _not_found_or_405(self):
        if self._is_collection():
            self._error(405, "method not allowed", allow="GET, POST")
        elif self.path.startswith("/api/") and self._task_id():
            self._error(405, "method not allowed", allow="PATCH, DELETE")
        else:
            self._error(404, "not found")

    # ---- routes ----
    def do_GET(self):
        if self._is_collection():
            try:
                tasks = self.store.list_tasks()
            except StorageError:
                return self._error(500, "storage failure")
            return self._send(200, {"tasks": tasks})
        if self.path.startswith("/api/"):
            return self._not_found_or_405()
        self._serve_static()

    def do_POST(self):
        if not self._is_collection():
            return self._not_found_or_405()
        body = self._read_json()
        if body is None:
            return self._error(400, "invalid JSON body")
        title = body.get("title")
        if not isinstance(title, str):
            return self._error(400, "title must be a string")
        try:
            task = self.store.add_task(title)
        except StorageError:
            return self._error(500, "storage failure")
        except ValueError as e:
            return self._error(400, str(e))
        self._send(201, {"task": task})

    def do_PATCH(self):
        task_id = self._task_id()
        if task_id is None:
            return self._not_found_or_405()
        body = self._read_json()
        if body is None or not isinstance(body.get("done"), bool):
            return self._error(400, "body must be JSON with boolean 'done'")
        try:
            task = self.store.update_task(task_id, body["done"])
        except StorageError:
            return self._error(500, "storage failure")
        except KeyError:
            return self._error(404, "task not found")
        self._send(200, {"task": task})

    def do_DELETE(self):
        task_id = self._task_id()
        if task_id is None:
            return self._not_found_or_405()
        try:
            self.store.delete_task(task_id)
        except StorageError:
            return self._error(500, "storage failure")
        except KeyError:
            return self._error(404, "task not found")
        self._send(204)

    def do_PUT(self):
        self._not_found_or_405()

    def _serve_static(self):
        rel = self.path.split("?", 1)[0].lstrip("/") or "index.html"
        target = (STATIC_DIR / rel).resolve()
        if STATIC_DIR not in target.parents or not target.is_file():
            return self._error(404, "not found")
        ctype = TYPES.get(target.suffix) or mimetypes.guess_type(target.name)[0] \
            or "application/octet-stream"
        data = target.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def create_server(port, data_path):
    """Build (but do not start) a server bound to 127.0.0.1:port (0 = any free port)."""
    handler = type("BoundHandler", (Handler,), {"store": TaskStore(data_path)})
    return ThreadingHTTPServer(("127.0.0.1", port), handler)


def main():
    parser = argparse.ArgumentParser(description="Taskboard server")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--data", default="tasks.json")
    args = parser.parse_args()
    server = create_server(args.port, args.data)
    print("Taskboard listening on http://127.0.0.1:%d" % server.server_address[1])
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
