from storage import load_tasks, save_tasks

def add_task(path, title):
    tasks = load_tasks(path)
    task_id = max((t["id"] for t in tasks), default=0) + 1
    tasks.append({"id": task_id, "title": title, "done": False, "archived": False})
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

def archive_task(path, task_id):
    tasks = load_tasks(path)
    for t in tasks:
        if t["id"] == task_id:
            t["archived"] = True
            save_tasks(path, tasks)
            return True
    return False

def list_tasks(path, include_archived=False):
    tasks = load_tasks(path)
    if include_archived:
        return tasks
    return [t for t in tasks if not t.get("archived", False)]
