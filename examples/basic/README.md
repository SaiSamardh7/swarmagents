# Basic — your first swarmagents run

The smallest useful invocation: one sentence of product intent, and the orchestrator runs the whole pipeline.

## Run

With the skill installed in Claude Code, describe a substantial build:

```
/swarmagents Build a small recipe box app: save a recipe (title, ingredients,
steps), list them, search by ingredient. Local persistence, no frameworks.
```

## What happens, phase by phase

1. **Intake** — the orchestrator inspects your repo (stack, tests, delivery setup) before asking anything the code can answer.
2. **Requirements** — you get **at most three** batched, decision-relevant questions (e.g. "single user or shared?"). Implementation details it can infer are recorded as assumptions, not questions.
3. **Blueprint** — scope, acceptance criteria, and assumptions are surfaced to you before any code is written.
4. **Waves** — work is split into contract-bound items with disjoint file ownership; independent frontend/backend/data items run as parallel workers (or serially, disclosed, if delegation is unavailable in your runtime).
5. **Gates** — an independent QA coordinator derives tests from the acceptance criteria; an independent reviewer examines the integrated diff. Failures go through the managerial recovery loop, not blind retries.
6. **Approval** — the run ends with a prepared delivery package and a question naming the exact mutation:

   > Approve pushing branch `swarm/recipe-box` to `origin` and creating a pull request against `main` with the prepared title and description?

   Silence is a no. Nothing is pushed, merged, or deployed until you approve that named action.

## What you get

A working, tested change plus the orchestration record (blueprint, work graph, worker results, gate outcomes). For a completed, committed run of exactly this pipeline, see [the taskboard reference build](../../demo/taskboard/).
