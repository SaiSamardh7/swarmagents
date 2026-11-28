# Requirements: Resume taskman-plus (run-01)

## 1. Status

Done and verified (do NOT modify; hashes recorded in workgraph.yml, grade.py checks byte-identity):
- BLD-01 storage.py (`load_tasks`, `save_tasks`; JSON file, missing file -> `[]`)
- BLD-02 core.py (`add_task`, `complete_task`, `list_tasks`; task = `{"id": int, "title": str, "done": bool}`)
- BLD-03 cli.py (add / done / list); covered by tests/test_base.py

Pending (status: ready):
- BLD-04 export.py, acceptance tests/test_export.py
- BLD-05 stats.py, acceptance tests/test_stats.py

Constraints: implement only export.py and stats.py at the project root (tests import `export`, `stats` as top-level modules); do not touch done files, tests/, or the workgraph's done entries; stdlib only. Suite command: `python3 -m unittest discover -s tests -t .`

## 2. Module requirements

### export.py
- R-EXP-1: `export_tasks(path, fmt)` loads tasks via `storage.load_tasks` (or `core.list_tasks`) and returns a string.
- R-EXP-2: fmt `"json"` returns valid JSON array of task objects, preserving order and fields (id, title, done).
- R-EXP-3: fmt `"csv"` returns text whose first line is exactly `id,title,done`, followed by one row per task in order; `done` rendered as Python bool text (`True`/`False`), e.g. `1,a,False`. Lines must be splitlines-compatible (titles with commas/quotes should be escaped via csv module; use `lineterminator="\n"`).
- R-EXP-4: any other fmt raises `ValueError`.

### stats.py
- R-STA-1: `stats(path)` returns dict `{"total": n, "done": n, "open": n}`.
- R-STA-2: total = number of tasks, done = tasks with `done` true, open = total - done.
- R-STA-3: a nonexistent/empty store yields all zeros (storage already returns `[]`).

## 3. Acceptance criteria

| ID | Criterion | Test |
|----|-----------|------|
| AC-01 | JSON export parses; titles are `["a","b"]` in order; second task `done` is true | tests/test_export.py::TestExport.test_export_json |
| AC-02 | CSV export header is `id,title,done` | tests/test_export.py::TestExport.test_export_csv (lines[0]) |
| AC-03 | CSV rows are `1,a,False` and `2,b,True` | tests/test_export.py::TestExport.test_export_csv (lines[1], lines[2]) |
| AC-04 | Unsupported format (`"xml"`) raises ValueError | tests/test_export.py::TestExport.test_export_bad_format |
| AC-05 | stats of 3 tasks (1 done) equals `{"total":3,"done":1,"open":2}` | tests/test_stats.py::TestStats.test_stats_counts |
| AC-06 | stats of missing/empty store equals all zeros | tests/test_stats.py::TestStats.test_stats_empty |
| AC-07 | Existing base tests still pass (regression) | tests/test_base.py (test_add_and_list, test_complete, test_complete_missing) |
| AC-08 | Done artifacts storage.py, core.py, cli.py are byte-identical to workgraph sha256; tests/ unmodified | grade.py (hash check); `git diff`/sha256sum |
| AC-09 | Full suite passes: `python3 -m unittest discover -s tests -t .` | all tests |
