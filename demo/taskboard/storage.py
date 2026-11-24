"""JSON-file backed task storage."""
import json
import os
import tempfile
import threading
import uuid
from datetime import datetime, timezone

MAX_TITLE = 200


class StorageError(ValueError):
    """The backing file is unreadable or corrupt (a server-side failure)."""


class TaskStore:
    def __init__(self, path):
        self._path = os.fspath(path)
        self._lock = threading.Lock()

    def _load(self):
        try:
            with open(self._path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            return []
        except (OSError, json.JSONDecodeError, UnicodeDecodeError) as e:
            raise StorageError("Cannot read task file %s: %s" % (self._path, e))
        if not isinstance(data, list):
            raise StorageError("Task file %s is corrupt: expected a JSON list" % self._path)
        return data

    def _save(self, tasks):
        """Atomic write: temp file in same directory, then os.replace."""
        directory = os.path.dirname(os.path.abspath(self._path))
        fd, tmp = tempfile.mkstemp(dir=directory, suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(tasks, f, indent=2)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp, self._path)
        except BaseException:
            if os.path.exists(tmp):
                os.unlink(tmp)
            raise

    @staticmethod
    def _find(tasks, task_id):
        for t in tasks:
            if t["id"] == task_id:
                return t
        raise KeyError(task_id)

    def list_tasks(self):
        with self._lock:
            tasks = self._load()
        # File is stored in insertion order; reversing first makes the stable
        # sort break created_at ties newest-inserted first.
        return sorted(reversed(tasks), key=lambda t: t["created_at"], reverse=True)

    def add_task(self, title):
        title = title.strip() if isinstance(title, str) else ""
        if not title:
            raise ValueError("title must not be empty")
        if len(title) > MAX_TITLE:
            raise ValueError("title must be at most %d characters" % MAX_TITLE)
        with self._lock:
            tasks = self._load()
            existing = {t["id"] for t in tasks}
            task_id = uuid.uuid4().hex[:8]
            while task_id in existing:
                task_id = uuid.uuid4().hex[:8]
            task = {
                "id": task_id,
                "title": title,
                "done": False,
                "created_at": datetime.now(timezone.utc).isoformat(timespec="microseconds"),
            }
            tasks.append(task)
            self._save(tasks)
        return dict(task)

    def update_task(self, task_id, done):
        with self._lock:
            tasks = self._load()
            task = self._find(tasks, task_id)
            task["done"] = bool(done)
            self._save(tasks)
            return dict(task)

    def delete_task(self, task_id):
        with self._lock:
            tasks = self._load()
            tasks.remove(self._find(tasks, task_id))
            self._save(tasks)
