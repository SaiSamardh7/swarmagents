# Task 3: Cross-layer feature — archive tasks

`taskman` is a tiny task manager: `storage.py` (JSON persistence), `core.py` (logic),
`cli.py` (command-line frontend). Add an **archive** feature across all three layers:

- Storage: tasks persist an `archived` field (default false); old files without it still load.
- Core: `archive_task(path, task_id)` marks a task archived; `list_tasks(path)` excludes
  archived tasks by default; `list_tasks(path, include_archived=True)` includes them.
- CLI: `archive <id>` command; `list --archived` flag includes archived tasks.

`tests/test_archive.py` specifies the feature and currently fails. Make the whole suite pass
(`python3 -m unittest discover -s tests`) without modifying any test file.
