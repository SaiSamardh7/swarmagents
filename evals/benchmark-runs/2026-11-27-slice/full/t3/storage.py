import json, pathlib

def _normalize(task):
    if isinstance(task, dict):
        task.setdefault("archived", False)
    return task

def load_tasks(path):
    p = pathlib.Path(path)
    if not p.exists():
        return []
    return [_normalize(t) for t in json.loads(p.read_text(encoding="utf-8"))]

def save_tasks(path, tasks):
    tasks = [_normalize(t) for t in tasks]
    pathlib.Path(path).write_text(json.dumps(tasks, indent=2), encoding="utf-8")
