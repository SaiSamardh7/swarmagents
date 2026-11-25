# Taskboard — the completed, committed run

This example is real, not hypothetical: the app and every orchestration artifact live in this repository at [`demo/taskboard/`](../../demo/taskboard/).

Three parallel builders (storage, API, frontend) coded against [versioned contracts](../../demo/taskboard/artifacts/contracts-v1.md) without seeing each other's code; an independent QA gate ran 31 tests against the real integrated stack; an independent review gate found issues that were fixed through the recovery loop before delivery. Read the [blueprint](../../demo/taskboard/artifacts/blueprint.md), the [wave manifest](../../demo/taskboard/artifacts/wave-1-manifest.md), the [worker results](../../demo/taskboard/artifacts/worker-results.md) (including what each builder did *not* verify), and both gate reports ([QA](../../demo/taskboard/artifacts/qa-report.md), [review](../../demo/taskboard/artifacts/review-report.md)).

Run the result:

```bash
cd demo/taskboard
python3 server.py        # http://127.0.0.1:8765
```
