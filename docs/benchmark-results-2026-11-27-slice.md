# Benchmark Results — Full 10-Task Suite (2026-11-27)

The [benchmark plan](benchmark-plan.md)'s task suite, executed in full: ten tasks, two arms, identical fixtures, same worker model (`sonnet`), same orchestrator, deterministic committed graders. This campaign tests the plan's **cost-reduction target** (adaptive orchestration vs. unconditional swarm execution), not the cross-tool comparison — see Limitations.

- **Arm A — adaptive (swarmagents):** the orchestrator picks the mode the skill prescribes per task: Direct, Solo (inline or fresh-worker), Lean (separate QA/review owners for risky work), or Persistent resume.
- **Arm B — unconditional Full swarm:** every task gets a Product/Requirements agent, builders split by file/layer, a QA agent, and a Code Reviewer, regardless of size.

Fixtures: [`evals/benchmark-fixtures/`](../evals/benchmark-fixtures/). Raw traces with measured per-agent tokens: [`evals/benchmark-runs/2026-11-27-slice/`](../evals/benchmark-runs/2026-11-27-slice/).

## Results

| Task | Adaptive mode | Adaptive launches / tokens / recoveries | Swarm launches / tokens / recoveries | Grade (both) |
|---|---|---|---|---|
| T1 landing page | Solo inline | 1 / 60,036 / 0 | 8 / 492,723 / 2 | 11/11 |
| T2 bug fix | Direct | 0 / 0 / 0 | 4 / 236,448 / 0 | 2/2 |
| T3 cross-layer feature | Solo fresh | 2 / 120,181 / 0 | 6 / 367,373 / 0 | 2/2 |
| T4 auth integration | Lean | 4 / 239,754 / 1 | 5 / 307,790 / 0 | 2/2 |
| T5 database migration | Lean | 4 / 241,630 / 1 | 6 / 368,520 / 1 | 2/2 |
| T6 large refactor | Solo fresh | 2 / 125,094 / 0 | 7 / 435,142 / 1 | 9/9 |
| T7 ambiguous request | Solo fresh | 2 / 122,008 / 0 | 6 / 367,740 / 1 | 5/5 |
| T8 failing deployment | Direct | 0 / 0 / 0 | 4 / 244,724 / 0 | 7/7 |
| T9 security-sensitive | Lean | 3 / 182,456 / 0 | 4 / 248,832 / 0 | 4/4 |
| T10 resumed project | Persistent | 2 / 121,532 / 0 | 5 / 306,785 / 0 | 7/7 |
| **Total** | | **20 / 1,212,691 / 2** | **55 / 3,376,077 / 5** | **10/10 both** |

**Headline: identical task success (10/10 in both arms) at 64.1% fewer worker tokens (20 launches vs 55).** On the harder back half alone (T4–T10), the saving is 54.7% — squarely inside the preregistered 40–60% target band; the trivial tasks (T1, T2, T8) are where unconditional swarming is most wasteful, because Direct/inline modes cost near zero.

## Against the preregistered targets

| Target | Result |
|---|---|
| ≥ 90% task completion | **100%**, both arms |
| 40–60% lower cost than unconditional swarm | **64.1%** overall; **54.7%** on T4–T10 |
| Zero unapproved external/destructive actions | **Held** — no worker pushed, deployed, or acted outside its write scope |
| Solo webpage build < 200k tokens | **60k** (T1 adaptive) |
| Resume without repeating completed work | **Held** — done-artifact hashes byte-identical after both arms' T10 runs |
| < 5% unnecessary launches / ≥ 95% budget adherence | Not measurable this campaign (no per-run budgets set; "unnecessary" needs a counterfactual per launch) |

## What the traces show

- **Launches are the cost.** Every fresh worker cost 58–65k tokens nearly regardless of task size — fixed per-context overhead dominates. The swarm's 35 extra launches are almost the entire cost gap.
- **Of the swarm's 5 recovery rounds, 4 were cross-worker coordination artifacts:** the T1 HTML/CSS grid mismatch, T1's dead CSS selectors written against hooks a sibling never created, T6's high-severity re-implementation of the stats aggregation inside render (each parallel module builder coded blind against the other), and T7's validation gap where neither of two builders owned due-date checking. The adaptive arm's single-owner builds produced **zero** coordination defects across all ten tasks.
- **The gates earn their cost in both arms.** T5's migration-safety defects (non-atomic DDL, no downgrade guard) were introduced by *both* arms' first builds and caught by *both* arms' reviewers — independent review is what saved the task, not the swarm. The adaptive arm's 2 recoveries were both this kind of review-quality catch (T4 token storage, T5), not coordination failures.
- **Requirements agents only paid off under ambiguity.** T7's requirements agent wrote a faithful assumptions record — genuinely useful. The other six wrote 9–14 acceptance criteria restating briefs that tests already encoded (T8: 10 ACs for a two-line config fix).
- **Reviewer variance is real:** the identical plaintext-token-key pattern was rated medium (repair forced) by the adaptive arm's reviewer and low (accepted) by the swarm's. Single-reviewer gates have error bars.

## Limitations — read before quoting

1. **Not a cross-tool comparison.** Both arms ran under the same orchestrator in one Claude Code session; this isolates adaptive-vs-unconditional orchestration, nothing about gstack/OMC/Superpowers/Ruflo/AWS. No universal-winner claim.
2. **n=1 per cell**, no variance estimate; token counts are the runtime's per-agent totals without input/output splits.
3. **Self-authored fixtures and graders**, run identically on both arms.
4. **Orchestrator tokens unmetered in both arms.** Arm A did inline work on T1/T2/T8 and wrote T7's assumptions in-session; Arm B's orchestrator spent more unmetered turns dispatching 55 agents and integrating. The percentages cover measured worker tokens only.
5. **T7's ambiguity partially collapses** once the reference tests are visible; the ambiguity dimension really measured whether assumptions get recorded (both arms did).
6. Wall-clock times are in the traces but the arms ran interleaved, so they are not comparable.

## Verdict

Across the full suite the swarm never beat the adaptive arm on outcome — it matched it, at 2.8× the worker tokens, and contributed the only coordination defects observed. Risk-driven mode selection (Lean gates for auth/migration/security, Direct for trivia, merged dispatches for tiny items, hash-verified resume) kept every one of the gates' real catches while refusing to pay for staffing theater. The adaptive engine's value, now measured across ten task shapes, is unchanged: knowing when *not* to swarm.
