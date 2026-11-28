from datetime import date
from storage import load_tasks, save_tasks

def add_task(path, title, due=None):
    tasks = load_tasks(path)
    task_id = max((t["id"] for t in tasks), default=0) + 1
    tasks.append({"id": task_id, "title": title, "done": False}
                 | ({"due": due} if due else {}))
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
    today = (today or date.today()).isoformat()
    return [t for t in load_tasks(path)
            if not t["done"] and t.get("due") and t["due"] < today]
