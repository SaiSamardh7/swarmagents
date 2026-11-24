# Evals — do the gates actually fire?

swarmagents makes behavioral claims: no external mutation without a named approval, no deploy without independent QA and review, no self-review, disclosed serial fallback, no orchestration theater for trivial edits. These scenarios probe each claim adversarially.

## Layout

- `scenarios/*.json` — one scenario per file: the adversarial `prompt`, heuristic `must_match` / `must_not_match` regexes applied to the transcript, and `grading_notes` for the human pass.
- `run.py` — zero-dependency runner. For each scenario it creates a temp workspace with the skill installed, runs `claude -p` (Claude Code headless; the CLI must be on PATH and authenticated), captures the transcript to `results/<scenario>.txt`, and applies the regexes.

## Run

```bash
python3 evals/run.py            # all scenarios
python3 evals/run.py no-push    # substring filter
```

Each scenario costs real model tokens. Results are **heuristic**: `PASS`/`FAIL` from the regexes, `REVIEW` when signals conflict. Regex grading of free-form transcripts can mislabel — read the saved transcript and `grading_notes` before trusting any single verdict; the scenario's claim is violated only if the transcript shows the forbidden behavior, not merely the forbidden words.

Structure tests (free, no model calls) live in `/tests` and run in CI; evals are run manually because they need an authenticated CLI and spend tokens.
