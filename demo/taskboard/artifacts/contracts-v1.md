# Shared contracts v1 — Taskboard demo

Versioned interface contracts for wave 1. A worker may not change these; a needed change is a blocker reported to the Orchestrator, who issues contracts v2 to every affected owner.

## C1. Task object (JSON)

```json
{"id": "8-char-hex", "title": "string (1-200 chars, stripped)", "done": false, "created_at": "ISO-8601 UTC"}
```

## C2. Storage interface (`storage.py` — owner: Database/Integration)

```python
class TaskStore:
    def __init__(self, path: str | os.PathLike): ...
    def list_tasks(self) -> list[dict]      # newest first
    def add_task(self, title: str) -> dict  # raises ValueError on empty/overlong title
    def update_task(self, task_id: str, done: bool) -> dict  # raises KeyError if unknown
    def delete_task(self, task_id: str) -> None              # raises KeyError if unknown
```

- Persists to a JSON file at `path`; file may not exist initially (treat as empty list).
- Atomic writes (temp file + `os.replace`), guarded by an internal `threading.Lock`.
- Standard library only.

## C3. HTTP API (`server.py` — owner: Backend)

| Method & path | Request body | Success | Errors |
|---|---|---|---|
| `GET /api/tasks` | — | 200 `{"tasks": [Task, …]}` | — |
| `POST /api/tasks` | `{"title": str}` | 201 `{"task": Task}` | 400 `{"error": str}` empty/missing/overlong title or invalid JSON |
| `PATCH /api/tasks/{id}` | `{"done": bool}` | 200 `{"task": Task}` | 400 invalid body · 404 `{"error": str}` unknown id |
| `DELETE /api/tasks/{id}` | — | 204 (no body) | 404 unknown id |

- `ThreadingHTTPServer` + `BaseHTTPRequestHandler`, stdlib only.
- All JSON responses `Content-Type: application/json`.
- Serves `static/index.html` at `/` and files under `static/` for other non-API paths (no directory traversal: resolve and verify the path stays inside `static/`).
- CLI: `python3 server.py [--port 8765] [--data tasks.json]`. Must expose `create_server(port, data_path) -> ThreadingHTTPServer` so tests can start it on port 0.
- Depends only on contract C2, not on storage internals.

## C4. Frontend (`static/` — owner: Frontend)

- Vanilla HTML/CSS/JS, no frameworks, no CDN. Calls the C3 API with `fetch` at relative paths.
- Behaviors: render list (newest first), add via form submit, toggle done via checkbox, delete via button. Re-render from the API response after each mutation; surface API errors in a visible status element.
- Accessible: form input has a `<label>`, buttons have text or `aria-label`, works at phone width.

## File ownership (hard boundary)

Each owner writes only the files in their blueprint row. Shared understanding flows through this document, never through editing another owner's file.
