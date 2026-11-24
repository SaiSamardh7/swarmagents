# Wave 1 worker results — as returned to the Orchestrator

Condensed from the three builders' structured hand-backs (contracts v1, disjoint write scopes, run concurrently). Full format in [../../../skills/swarmagents/references/contracts.md](../../../skills/swarmagents/references/contracts.md).

## W1 · builder-data → `storage.py`

- **Artifacts:** `storage.py` (88 lines, stdlib only)
- **Verification (self-smoke in temp dir):** empty-on-missing-file; strip/validate title; newest-first ordering; persistence across a fresh `TaskStore` (reload from disk); ValueError on empty/201-char title; KeyError on unknown id (update + delete); 20 concurrent `add_task` threads → no loss; corrupt JSON raises ValueError and leaves the file untouched; no leftover temp files.
- **Blockers:** none. **Notes:** atomic write via `mkstemp` + fsync + `os.replace`; returned dicts are copies.

## W2 · builder-backend → `server.py`

- **Artifacts:** `server.py` (~150 lines, stdlib only; `create_server(port, data_path)` for tests, binds 127.0.0.1)
- **Verification (against a FAKE in-memory store in a temp workspace — the real `storage.py` did not exist yet):** all four endpoints to contract; 400s for invalid JSON/empty title/non-bool `done`; 404s for unknown ids and routes; 405 for wrong method; static serving of `/` and files with correct Content-Type; path-traversal probes (`/../`, `/%2e%2e/`) → 404.
- **Blockers:** none. **Notes:** integration with the real store deferred to the QA gate, as scheduled.

## W3 · builder-frontend → `static/index.html`, `static/app.js`, `static/style.css`

- **Verification (static checks only):** tags balanced; label/for ↔ input id; every id referenced by `app.js` exists; `role="status"` error surface; titles rendered via `textContent` (no `innerHTML` with user data); re-render from server after each mutation; 204 handled; empty state; ~70-line CSS with dark mode, focus-visible, 375px-wide support.
- **Blockers:** none. **Notes:** live API never called — end-to-end deferred to the QA gate.

## Orchestrator integration decision

Write scopes disjoint → integrate all three as-is. Known gap for the QA gate: **no component has run against another real component yet.** QA must cover store units, live HTTP API against the real store, persistence across restart, and static serving of the real frontend files.
