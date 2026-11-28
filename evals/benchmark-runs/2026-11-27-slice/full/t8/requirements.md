# Requirements: Task 8, Failing deployment

## Observed failure chain
1. `python3 build.py` exits 1 with `json.decoder.JSONDecodeError: Expecting value: line 7 column 3 (char 251)` at `json.loads` in `main()`. No output is produced and `dist/` is never created.
2. Line 7 col 3 is the `]` that closes `pages`. The previous line (the `about` page object) ends with a trailing comma, which is invalid JSON.
3. Latent second failure (not yet observable, because step 1 hides it; found by reading). `templates/index.tmpl` uses `{contact_email}`. `site.json` `defaults` only has `tagline`, and the `index` page has no `contact_email`. After the JSON is fixed, `template.format(**variables)` raises `KeyError: 'contact_email'` on the first page.
4. Other checks. `about.tmpl` needs `title` and `body`, and both are supplied. `out.mkdir(exist_ok=True)` and overwrite-on-write make a second run safe. No stray braces exist in the templates. No other defects were found by reading.

## Root-cause hypotheses
- H1 (confirmed): the trailing comma in `site.json` after the `about` object.
- H2 (high confidence, derived from reading): `contact_email` is missing from the config. The correct fix is data, not code or template: add a plausible address to `defaults` in `site.json`, e.g. `"contact_email": "hello@acme.example"`.
- H3 (rejected fixes, per the brief): removing `{contact_email}` from the template or using `format_map`/`.get` with an empty default would weaken the templates. Wrapping the build in try/except would swallow errors.

## Scope and constraints
- Allowed edit surface: `site.json` only. `build.py` and `templates/` should stay unchanged.
- The contact email must still render as a plausible address.
- `build.py` must not swallow errors.
- The build must succeed twice in a row.

## Acceptance criteria
- AC1: `site.json` parses as strict JSON (`python3 -c "import json;json.load(open('site.json'))"` exits 0). The trailing comma is removed.
- AC2: `python3 build.py` exits 0 and prints `built index` and `built about`.
- AC3: `dist/index.html` and `dist/about.html` both exist after the build.
- AC4: `dist/index.html` contains `<title>Acme Home</title>`. `dist/about.html` contains `<title>About Acme</title>`. These match the configured titles.
- AC5: `dist/index.html` renders `Contact:` followed by a plausible email address. It must match `[\w.+-]+@[\w-]+(\.[\w-]+)+`, and no literal `{contact_email}` or empty value may remain.
- AC6: `contact_email` is supplied via `site.json` (`defaults`). `templates/*.tmpl` is byte-identical to the original and still contains `{contact_email}`.
- AC7: `build.py` still has no blanket `except`, `try/except` suppression, or `format_map`/default-masking of missing keys. It remains byte-identical, or any change preserves strict failure on error. A missing variable must still raise.
- AC8: Running `python3 build.py` twice consecutively exits 0 both times, and the outputs are identical.
- AC9: The rendered tagline (`We make things.`) and the about body (`Founded 2020.`) appear in the correct pages. The existing defaults and page values are preserved.
- AC10: No files other than `site.json` (and the generated `dist/`) are changed by the repair.
