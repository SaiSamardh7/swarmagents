# Taskboard — the swarmagents reference build

A minimal task board (vanilla JS frontend, stdlib-only Python API, JSON persistence) built **by the swarmagents process itself**: one orchestrator, three parallel builders with disjoint file ownership coding against versioned contracts, then an independent QA gate and code-review gate. The point isn't the app — it's the published paper trail.

## The proof artifacts

| Artifact | What it shows |
|---|---|
| [artifacts/blueprint.md](artifacts/blueprint.md) | Scope, acceptance criteria, recorded assumptions, team & ownership |
| [artifacts/contracts-v1.md](artifacts/contracts-v1.md) | The versioned interface contracts the parallel builders coded against |
| [artifacts/wave-1-manifest.md](artifacts/wave-1-manifest.md) | The dispatch manifest: write-scope disjointness + readiness checks |
| [artifacts/worker-results.md](artifacts/worker-results.md) | Each builder's structured hand-back, including what was NOT yet verified |
| [artifacts/qa-report.md](artifacts/qa-report.md) | The independent QA gate run |
| [artifacts/review-report.md](artifacts/review-report.md) | The independent code-review gate findings and their resolution |

No builder tested against another builder's real code — integration risk was carried explicitly to the QA gate, which exercised the real stack end-to-end.

## Run it

```bash
cd demo/taskboard
python3 server.py            # http://127.0.0.1:8765, data in tasks.json
```

Python ≥ 3.9, zero dependencies.

## Test it

```bash
cd demo/taskboard
python3 -m unittest discover -s tests -v
```
