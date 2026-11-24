#!/usr/bin/env python3
"""Run swarmagents behavioral evals through Claude Code headless (`claude -p`).

Zero dependencies. Each scenario installs the skill into a temp workspace,
runs its adversarial prompt, saves the transcript under evals/results/, and
applies the scenario's heuristic regexes. Verdicts: PASS / FAIL / REVIEW.
Regex grading of free-form transcripts is heuristic — always read the saved
transcript and the scenario's grading_notes before trusting a verdict.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

EVALS_DIR = Path(__file__).resolve().parent
REPO_ROOT = EVALS_DIR.parent
SKILL_SRC = REPO_ROOT / "skills" / "swarmagents"
RESULTS = EVALS_DIR / "results"
TIMEOUT_S = 600


def load_scenarios(filter_substr):
    paths = sorted((EVALS_DIR / "scenarios").glob("*.json"))
    scenarios = [json.loads(p.read_text(encoding="utf-8")) for p in paths]
    if filter_substr:
        scenarios = [s for s in scenarios if filter_substr in s["name"]]
    return scenarios


def run_scenario(scenario):
    with tempfile.TemporaryDirectory(prefix="swarmagents-eval-") as ws:
        ws = Path(ws)
        shutil.copytree(SKILL_SRC, ws / ".claude" / "skills" / "swarmagents")
        (ws / "README.md").write_text("# eval-workspace\n\nA file with teh typo.\n", encoding="utf-8")
        subprocess.run(["git", "init", "-q"], cwd=ws, check=False)
        claude = shutil.which("claude")
        if not claude:
            sys.exit("error: `claude` CLI not found on PATH — install and authenticate Claude Code first.")
        try:
            proc = subprocess.run(
                [claude, "-p", scenario["prompt"], "--output-format", "text"],
                cwd=ws, capture_output=True, text=True, timeout=TIMEOUT_S,
            )
        except subprocess.TimeoutExpired:
            return "REVIEW", f"(timed out after {TIMEOUT_S}s)"
        transcript = proc.stdout + ("\n--- stderr ---\n" + proc.stderr if proc.stderr.strip() else "")

    missing = [rx for rx in scenario.get("must_match", []) if not re.search(rx, transcript)]
    forbidden = [rx for rx in scenario.get("must_not_match", []) if re.search(rx, transcript)]
    if forbidden:
        verdict = "FAIL"
    elif missing:
        verdict = "REVIEW"
    else:
        verdict = "PASS"
    detail = "; ".join(
        [f"matched forbidden: {rx}" for rx in forbidden] + [f"missing expected: {rx}" for rx in missing]
    ) or "all heuristics satisfied"
    return verdict, detail, transcript


def main():
    filter_substr = sys.argv[1] if len(sys.argv) > 1 else None
    scenarios = load_scenarios(filter_substr)
    if not scenarios:
        sys.exit(f"no scenarios match {filter_substr!r}")
    RESULTS.mkdir(exist_ok=True)
    failures = 0
    for s in scenarios:
        print(f"[{s['name']}] running...", flush=True)
        result = run_scenario(s)
        verdict, detail = result[0], result[1]
        if len(result) == 3:
            out = RESULTS / f"{s['name']}.txt"
            out.write_text(result[2], encoding="utf-8")
            print(f"[{s['name']}] {verdict} — {detail}\n  transcript: {out}")
        else:
            print(f"[{s['name']}] {verdict} — {detail}")
        failures += verdict == "FAIL"
    print(f"\n{len(scenarios)} scenario(s); {failures} heuristic FAIL(s). "
          "Read transcripts + grading_notes before trusting verdicts.")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
