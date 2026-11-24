# QA gate report — Taskboard demo

**Gate:** Tester/QA (independent of all three authors) · **Date:** 2026-11-24 · **Verdict: PASS**

## Command & result

```
cd demo/taskboard && python3 -m unittest discover -s tests -v
Ran 31 tests in 9.2s — OK (31 passed, 0 failed, 0 errors)
```

Every server test ran the **real** `create_server(0, <temp data file>)` with the **real** `TaskStore` — this gate is where the independently built components first met, as scheduled in the wave manifest.

## Coverage against acceptance criteria

| Criterion | Evidence |
|---|---|
| List + newest-first ordering | `test_list_newest_first` (unit + through the API) |
| Create happy path & rejection | 201 on valid; 400 on empty/overlong title, invalid JSON, non-object body; exactly-200-char title accepted |
| Toggle + errors | 200 on valid PATCH; 400 non-bool body; 404 unknown id |
| Delete + errors | 204; 404 unknown id; second DELETE 404 |
| Persistence | `test_persistence_across_server_restart` (new store + new server, same file); corrupt-JSON ValueError; no leftover temp files |
| Static serving & traversal | `/`, `/style.css`, `/app.js` served; raw-socket probes `/../server.py`, `/%2e%2e/…`, `/../../etc/passwd` → 404, no source leaked |
| Concurrency | 20-thread `add_task` burst, no loss |

14 storage unit tests + 17 API/static tests = 31. Raw sockets were used for traversal probes so client-side path normalization couldn't mask a server flaw.

## Observations passed to review (non-blocking)

- Suite takes ~9s, dominated by per-write `fsync` — a durability choice, not a defect.
- Default per-request logging clutters stderr during tests.
