from storage import load_tasks, save_tasks

def add_task(path, title):
    tasks = load_tasks(path)
    task_id = max((t["id"] for t in tasks), default=0) + 1
    tasks.append({"id": task_id, "title": title, "done": False})
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
