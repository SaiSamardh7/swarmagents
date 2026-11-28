# Task 7: Ambiguous product request

> "People keep missing overdue work in taskman. Do something about it."

That is the entire request. No user is available to answer questions in this
benchmark, so: write the clarifying questions you *would* ask, and the assumptions
you proceed on, in `ASSUMPTIONS.md` — then implement your interpretation.

For gradability, `tests/test_overdue.py` encodes the reference interpretation
(optional due dates on add; `list_overdue(path, today=...)` returning undone tasks
whose due date has passed). Make the suite pass
(`python3 -m unittest discover -s tests -t .`) without modifying tests/, and add a
`--due YYYY-MM-DD` option to the CLI `add` command plus a `list --overdue` flag.
