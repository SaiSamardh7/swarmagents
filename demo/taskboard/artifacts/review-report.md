# Code-review gate report — Taskboard demo + orchestrator tooling

**Gate:** Code Reviewer (authored none of the reviewed code) · **Date:** 2026-11-24
**Scope:** `storage.py`, `server.py`, `static/*`, `tests/*`, plus orchestrator-authored `evals/run.py`, `/tests/test_structure.py`, `.github/workflows/ci.yml`
**Verdict: PASS** — no critical or high findings. One medium and four low findings were fixed before delivery; four nits were accepted with rationale.

## Findings fixed (recovery loop, verified by re-running both suites)

| Sev | Finding | Fix |
|---|---|---|
| Medium | Corrupt/unreadable data file surfaced as **400 with the server's absolute path in the response body** on POST, and as an unhandled exception (dropped connection) on GET/PATCH/DELETE | New `StorageError(ValueError)` raised by the store's loader; every route maps it to a generic `500 {"error": "storage failure"}` |
| Low | `Content-Length` trusted unbounded → arbitrary memory buffering | Bodies over 64 KiB (or negative lengths) rejected as invalid (400) |
| Low | 32-bit task ids (`uuid4().hex[:8]`) with no uniqueness check — a collision silently updates/deletes the wrong task | Id regenerated under the lock until unused |
| Low | `read_text`/`write_text` without `encoding="utf-8"` breaks on Windows locale encodings (evals runner, structure tests) | Explicit `encoding="utf-8"` everywhere |
| Low | `subprocess.run(["claude", …])` misses the `claude.cmd` shim on Windows | Resolved via `shutil.which` first |
| Nit | 405 responses lacked the RFC 9110 `Allow` header; dead `methods_for` parameter | `Allow: GET, POST` / `Allow: PATCH, DELETE` emitted; parameter removed |
| Nit | CI job ran with default (broad) token permissions | `permissions: contents: read` |

## Findings accepted as-is (recorded, not fixed)

- `fd` leak only if `os.fdopen` itself raises (vanishingly rare); stray `tmp*.tmp` survives only a kill between `mkstemp` and `os.replace` — both acceptable for a demo.
- Frontend has no in-flight guard: a double-click on Add before the POST resolves can create a duplicate. Acceptable demo scope.

## Verified-good (reviewer's positive assertions)

Path-traversal defense is sound (`resolve()` before a parent-containment check; the handler never percent-decodes, so `%2e%2e` can't match a real file). No XSS surface (`textContent`/`setAttribute` only, no `innerHTML`). Atomic write + fsync + `os.replace` correct and Windows-compatible; the lock covers every load-modify-save. Newest-first tie-break logic correct. Tests shut servers down cleanly and clean their temp dirs. Contracts C1–C4 faithfully implemented, including status-code semantics and 127.0.0.1-only binding.

## Post-fix verification

```
python3 -m unittest discover -s tests            # repo root: structure tests
cd demo/taskboard && python3 -m unittest discover -s tests   # 31 app tests
```

Both suites green after the fixes (run recorded in the delivery notes).
