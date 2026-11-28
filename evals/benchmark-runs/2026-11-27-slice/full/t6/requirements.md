# Requirements: Task 6, reporting refactor

## Context
`legacy.py` (74 lines) holds `summarize` and `generate_report`. Validation is copy-pasted three times (summarize, generate_report prelude, and a redundant second pass in the csv branch). Aggregation is duplicated between summarize and the text branch. A module-level `_CACHE` is written (`last`, `last_text`) but never read. `report/__init__.py` is a shim importing from `legacy`.

## Refactor constraints
- C1 Stdlib only. No new dependencies.
- C2 Module boundaries (under `report/`):
  - `validate.py`: record validation and normalization only.
  - `stats.py`: aggregation (total, count, average, per-category) only; no formatting, no validation.
  - `render.py`: text and csv formatting plus format dispatch; no validation, no aggregation.
  - `__init__.py`: exposes `generate_report` and `summarize` (may define them as thin orchestrators); no import from `legacy`.
- C3 Validation logic (the four checks plus normalization to `{"category": str, "amount": float}`) exists in exactly one place, in `validate.py`. Called once per public call (csv's second validation pass is removed).
- C4 Aggregation (total, per-category sums, count, average) exists once, in `stats.py`, shared by `summarize` and the text renderer.
- C5 No function in `report/` exceeds 40 lines (including `generate_report`).
- C6 Magic numbers and strings (column widths 12 and 10, rounding precision 2, format names, header strings) become named module-level constants.
- C7 The module-level `_CACHE` is removed. It is write-only, so removal does not alter returned values.
- C8 `legacy.py` is deleted. Nothing references `legacy`.
- C9 `tests/` is not modified.

## Behavior to preserve
- Validation order and exact messages: "record must be a dict"; "record needs category and amount"; "amount must be a number" (bool rejected, int/float accepted); "amount must be non-negative". Records are checked in input order, and the first failing record raises.
- Validation runs before the format check, so a bad record with an unknown format raises a validation error, not "unknown format". Also, an unknown format with valid records raises `ValueError("unknown format: <fmt>")`.
- summarize returns `{"total", "count", "average", "by_category"}`, with values rounded to 2 places and `by_category` sorted by key. An empty list gives `{"total": 0.0, "count": 0, "average": 0.0, "by_category": {}}`.
- Text report: "REPORT" header line; sorted category lines `"%-12s %10.2f"`; TOTAL line (unrounded total formatted `%10.2f`); COUNT line (`%10d`); AVERAGE line (average rounded to 2 places, `%10.2f`); joined with "\n", no trailing newline.
- CSV: header `category,amount`, then one line per record in input order (not sorted, not aggregated), `"%s,%.2f"`.
- Category is coerced with `str()`; amount is coerced with `float()`.

## Acceptance criteria
- AC-01 `python3 -m unittest discover -s tests -t .` passes with `tests/` byte-identical to the original.
- AC-02 `legacy.py` does not exist, and no file in the repo imports or mentions `legacy` in code.
- AC-03 `report/validate.py`, `report/stats.py`, `report/render.py` exist, and `report/__init__.py` exposes `generate_report` and `summarize`.
- AC-04 The four validation error messages appear exactly once in total across `report/` (all in `validate.py`).
- AC-05 No function or method in `report/` is longer than 40 lines (checked by AST).
- AC-06 `validate.py` has no formatting or aggregation code. `stats.py` has no validation or formatting code. `render.py` has no validation code.
- AC-07 `generate_report` and `summarize` validate each input exactly once per call.
- AC-08 Totals, counts, averages, and per-category sums are computed in one place (`stats.py`) and reused by both `summarize` and the text renderer.
- AC-09 No module-level mutable state (`_CACHE` or similar dict/list) in `report/`.
- AC-10 Output equivalence: for a corpus of inputs (the test RECS, empty list, single record, unicode and non-string categories, int and float amounts, zero amounts, rounding edge cases such as 0.005 and 2/3), `summarize` and `generate_report` with "text" and "csv" return values identical to the original `legacy.py` (verify against git history or a saved copy before deletion).
- AC-11 Error equivalence: for invalid inputs (non-dict, missing category, missing amount, bool amount, string amount, negative amount, bad format, bad record plus bad format), the exception type and message match the original.
- AC-12 Magic numbers (12, 10, 2) and the format names and header strings appear as named constants rather than inline literals in function bodies.
- AC-13 Only stdlib imports are used in `report/`.
- AC-14 `report/__init__.py` contains no import from `legacy`, and the shim comment is removed.
