# Web app — parallel builders at full width

A fuller brief that exercises wave scheduling: multiple pages, an API, and a schema, built by parallel workers that never touch each other's files.

## Run

```
/swarmagents Build a team bookmarks web app: shared link list with tags,
add/edit/delete, tag filter page, and a stats page (links per tag).
SQLite storage, server-rendered pages, keyboard accessible.
```

## What to expect

Before any builder starts, the orchestrator establishes the shared contracts for a web build — route and page map, design tokens, component boundaries, data types, API schemas, state ownership, and file ownership — following [parallel-web-build.md](../../skills/swarmagents/references/parallel-web-build.md):

- **Wave 0** — contracts and foundations (schema, tokens, route map).
- **Wave 1** — independent features in parallel: each page, endpoint group, and schema area is a separate work item with its own owner; frontend, backend, and data items run concurrently when independent.
- **Wave 2** — integration and quality: the orchestrator integrates at the wave barrier, then the QA and review gates run on the integrated candidate.

Two rules you should see enforced in practice:

- **No overlapping write scopes.** If two items would edit one file, ownership is reassigned or the items are serialized — collisions are prevented, not merged away.
- **Contract changes are versioned.** A builder that needs a different API shape reports a blocker; the orchestrator issues contracts v2 to every affected owner rather than letting one worker silently revise a shared interface.

The run still ends at the same place every run ends: a prepared delivery package and an approval question naming the exact push/PR, with deployment blocked until the QA and review gates have both passed.
