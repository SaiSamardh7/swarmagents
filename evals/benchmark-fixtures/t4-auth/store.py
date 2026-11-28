import json, pathlib

def new_store():
    return {"users": {}, "notes": {}, "tokens": {}}

def save_store(path, store):
    pathlib.Path(path).write_text(json.dumps(store, indent=2), encoding="utf-8")

def load_store(path):
    p = pathlib.Path(path)
    if not p.exists():
        return new_store()
    return json.loads(p.read_text(encoding="utf-8"))
