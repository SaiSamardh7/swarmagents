import json
from storage import load_tasks

def export_tasks(path, fmt):
    tasks = load_tasks(path)
    if fmt == "json":
        return json.dumps(tasks, indent=2)
    if fmt == "csv":
        rows = ["id,title,done"]
        for t in tasks:
            title = str(t["title"])
            if any(c in title for c in ',"\n'):
                title = '"' + title.replace('"', '""') + '"'
            rows.append(f'{t["id"]},{title},{t["done"]}')
        return "\n".join(rows) + "\n"
    raise ValueError(f"unsupported format: {fmt}")
