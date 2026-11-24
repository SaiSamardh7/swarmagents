# Blueprint — Taskboard demo (swarmagents reference build)

**Produced by:** Orchestrator, swarmagents v0.1.0 flow · **Date:** 2026-11-24
**Purpose:** A reproducible end-to-end proof that the swarmagents pipeline (contracts → parallel builders → QA gate → review gate) produces a working, tested artifact. This is the repository's demo, built by the process it documents.

## Product intent

A minimal team task board: list tasks, add a task, mark it done/undone, delete it. Single user, local persistence. No auth, no deploy — the delivery boundary for this demo is a verified local build (the approval-gated push was approved by the repository owner for this repo).

## Constraints

- **Zero dependencies.** Python 3 standard library only; vanilla HTML/CSS/JS frontend. Must run with `python3 server.py` on any machine with Python ≥3.9.
- All code lives under `demo/taskboard/`; tests under `demo/taskboard/tests/`.
- Thread-safe, atomic persistence (the server is threaded).

## Acceptance criteria

1. `GET /api/tasks` returns the persisted task list as JSON.
2. `POST /api/tasks` with a non-empty title creates a task (201); empty/missing title is rejected (400).
3. `PATCH /api/tasks/{id}` toggles `done` (200); unknown id → 404.
4. `DELETE /api/tasks/{id}` removes the task (204); unknown id → 404.
5. Tasks survive a server restart (JSON file persistence, atomic writes).
6. The frontend at `/` can list, add, toggle, and delete tasks against the live API.
7. Unit tests cover the store; API tests exercise every endpoint including error paths; all pass via `python3 -m unittest discover -s tests`.

## Assumptions (recorded, not asked)

- Port 8765 default, overridable via `--port`; data file `tasks.json`, overridable via `--data`.
- Task ordering: newest first in the API response.

## Team & ownership (wave 1)

| Work item | Group | Owner writes ONLY |
|---|---|---|
| W1 Storage layer | Database/Integration builder | `storage.py` |
| W2 HTTP API server | Backend builder | `server.py` |
| W3 Frontend | Frontend builder | `static/index.html`, `static/app.js`, `static/style.css` |
| W4 Tests (QA gate) | Tester/QA coordinator | `tests/` |
| W5 Review (review gate) | Code Reviewer | no files — findings only |

W1–W3 run in parallel against the versioned contracts in [contracts-v1.md](contracts-v1.md). W4 runs after integration; W5 after W4 passes.
