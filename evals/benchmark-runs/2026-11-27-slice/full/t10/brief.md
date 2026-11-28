# Task 10: Resume an interrupted project

This project was interrupted mid-run. Durable run state is in
`.swarmagents/runs/run-01/workgraph.yml`: three work items are done and verified
(storage.py, core.py, cli.py — `tests/test_base.py` passes), two are ready:

- `export.py`: `export_tasks(path, fmt)` returning the tasks serialized as `"json"`
  or `"csv"` (header `id,title,done`), raising `ValueError` on other formats.
- `stats.py`: `stats(path)` returning `{"total": n, "done": n, "open": n}`.

Resume and complete the project: implement only the ready items, do not redo or
rewrite the done artifacts, and make the whole suite pass
(`python3 -m unittest discover -s tests -t .`) without modifying tests/.
grade.py verifies the done files are byte-identical to their recorded hashes.
