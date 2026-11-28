from storage import load_tasks


def stats(path):
    tasks = load_tasks(path)
    done = sum(1 for t in tasks if t.get("done"))
    return {"total": len(tasks), "done": done, "open": len(tasks) - done}
