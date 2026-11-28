from datetime import date
from storage import load_tasks, save_tasks

def add_task(path, title, due=None):
    tasks = load_tasks(path)
    task_id = max((t["id"] for t in tasks), default=0) + 1
    task = {"id": task_id, "title": title, "done": False}
    if due is not None:
        try:
            date.fromisoformat(due)
        except TypeError:
            raise ValueError(f"invalid due date: {due!r}")
        task["due"] = due
    tasks.append(task)
    save_tasks(path, tasks)
    return task_id

def complete_task(path, task_id):
    tasks = load_tasks(path)
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
            save_tasks(path, tasks)
            return True
    return False

def list_tasks(path):
    return load_tasks(path)

def list_overdue(path, today=None):
    if today is None:
        today = date.today()
    out = []
    for t in load_tasks(path):
        if t.get("done") or not t.get("due"):
            continue
        try:
            if date.fromisoformat(t["due"]) < today:
                out.append(t)
        except (ValueError, TypeError):
            continue
    return out
