# Wave 1 manifest — Taskboard demo

**Dispatched:** 2026-11-24 · **Scheduler:** Orchestrator · **Contracts:** v1

| Item | Group | Agent | Write scope | Dependencies | Verification command |
|---|---|---|---|---|---|
| W1 Storage | Database/Integration | builder-data | `storage.py` | contracts C1, C2 | `python3 -c "import storage"` + QA tests |
| W2 API server | Backend | builder-backend | `server.py` | contracts C1, C2 (interface only), C3 | `python3 -c "import server"` + QA tests |
| W3 Frontend | Frontend | builder-frontend | `static/*` | contract C3, C4 | manual + API smoke via QA |

Overlap check: write scopes are disjoint. ✔
Ready check: all three depend only on v1 contracts, none on another's output. ✔ → all three dispatch concurrently.

Wave barrier: integrate only when all three worker results are in; then W4 (QA gate) → W5 (review gate).
