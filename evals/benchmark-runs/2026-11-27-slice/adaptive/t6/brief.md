# Task 6: Large refactor

`legacy.py` is a working but messy reporting monolith (duplicated validation in
three places, magic numbers, a module-level cache, one oversized function). The
tests import from the `report` package, which is currently just a shim re-exporting
legacy. Refactor, stdlib only, behavior unchanged:

- Move the logic into `report/validate.py`, `report/stats.py`, `report/render.py`,
  with `report/__init__.py` exposing `generate_report` and `summarize`.
- Delete `legacy.py` and the shim import; validation logic exists exactly once.
- No function longer than 40 lines anywhere in `report/`.

The suite (`python3 -m unittest discover -s tests -t .`) passes today and must still
pass, unmodified, afterward. grade.py also enforces the structure rules.
