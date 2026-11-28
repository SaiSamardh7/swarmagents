# Task 8: Failing deployment

`python3 build.py` is the deploy pipeline for a tiny static site and it currently
fails. Diagnose and repair until the build succeeds and produces `dist/index.html`
and `dist/about.html` with their configured titles. Rules: do not weaken the
templates (the contact email must still render as a plausible address), do not
swallow errors in build.py, and the build must succeed when run twice in a row.
