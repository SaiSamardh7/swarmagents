import csv, io, json
from storage import load_tasks

def export_tasks(path, fmt):
    if fmt not in ("json", "csv"):
        raise ValueError(f"unsupported format: {fmt!r}")
    tasks = load_tasks(path)
    if fmt == "json":
        return json.dumps(tasks)
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["id", "title", "done"])
    for t in tasks:
        w.writerow([t["id"], t["title"], t["done"]])
    return buf.getvalue()
