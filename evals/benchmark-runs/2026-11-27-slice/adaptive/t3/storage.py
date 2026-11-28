import json, pathlib

def load_tasks(path):
    p = pathlib.Path(path)
    if not p.exists():
        return []
    tasks = json.loads(p.read_text(encoding="utf-8"))
    for t in tasks:
        t.setdefault("archived", False)
    return tasks

def save_tasks(path, tasks):
    pathlib.Path(path).write_text(json.dumps(tasks, indent=2), encoding="utf-8")
