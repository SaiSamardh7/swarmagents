# Benchmark Results — 3-Task Slice (2026-11-27)

A first, small execution of the [benchmark plan](benchmark-plan.md): tasks 1–3 of the suite, run under two arms on identical fixtures. This slice tests the plan's **cost-reduction target** (adaptive orchestration vs. unconditional swarm execution), not the cross-tool comparison — see Limitations.

- **Arm A — adaptive (swarmagents):** the orchestrator selects the mode per the skill: Direct, Solo inline, or Solo fresh-worker as the work graph warrants.
- **Arm B — unconditional Full swarm:** every task gets a Product/Requirements agent, specialist builders split by file/layer, a QA agent, and a Code Reviewer, regardless of size.

Same fixtures, same worker model (`sonnet`), same orchestrator, same deterministic graders. Fixtures: [`evals/benchmark-fixtures/`](../evals/benchmark-fixtures/). Raw traces: [`evals/benchmark-runs/2026-11-27-slice/`](../evals/benchmark-runs/2026-11-27-slice/).

## Results

| Task | Arm | Mode | Worker launches | Measured worker tokens | Recovery rounds | Grade |
|---|---|---|---:|---:|---:|---|
| T1 landing page | adaptive | Solo (inline) | 1 | 60,036 | 0 | 11/11 |
| T1 landing page | full | swarm | 8 | 492,723 | 2 | 11/11 |
| T2 bug fix | adaptive | Direct | 0 | 0 | 0 | 2/2 |
| T2 bug fix | full | swarm | 4 | 236,448 | 0 | 2/2 |
| T3 cross-layer | adaptive | Solo (fresh) | 2 | 120,181 | 0 | 2/2 |
| T3 cross-layer | full | swarm | 6 | 367,373 | 0 | 2/2 |
| **Total** | **adaptive** | | **3** | **180,217** | **0** | 3/3 |
| **Total** | **full** | | **18** | **1,096,544** | **2** | 3/3 |

**Headline: identical task success (3/3 both arms), with the adaptive arm using 83.6% fewer worker tokens and 3 launches instead of 18.** That clears the plan's 40–60% cost-reduction target on this slice, with margin.

## What the traces show

- **Launches dominate cost.** Every fresh worker cost 59k–64k tokens almost regardless of its task — a one-character bug fix and a full feature build billed nearly the same, because per-worker context overhead is fixed. Unnecessary launches are therefore the single biggest cost lever, which is exactly what mode selection controls.
- **The swarm's defects were coordination artifacts.** Arm B's only recovery rounds came from splitting one page across single-file workers: an HTML/CSS grid-selector mismatch that silently disabled the responsive layout (invisible to the structural grader; caught at the integration barrier), and dead CSS selectors written against HTML hooks the sibling never created. The adaptive arm's single-owner builds produced zero cross-worker defects.
- **Requirements theater is real.** Arm B's requirements agent produced 42 acceptance criteria for a static landing page, at ~61k tokens, none of which changed what was built.
- **The swarm wasn't useless.** Arm B's reviewer found genuine low-severity issues (duplicated normalization across T3's layers, test gaps) that Arm A's single verifier also broadly caught. The gates earn their cost in both arms; the extra builders and requirements agents did not.

## Metrics not collected in this slice

Human corrections (none needed in either arm), dollar cost (rates not pinned for the runtime's internal models — token counts are reported instead), defects found by a later independent reviewer, and context-duplication measurement beyond launch counts. Wall-clock times are recorded in the traces but the arms ran interleaved in one session, so they are not comparable and are not reported as results.

## Limitations — read before quoting

1. **Not a cross-tool comparison.** Both arms were executed by the same orchestrator in one Claude Code session. This tests adaptive-vs-unconditional orchestration (the plan's cost target), not swarmagents vs. gstack/OMC/Superpowers/Ruflo/AWS. The universal-winner claim remains unsupported.
2. **Single run, n=1 per cell.** No variance estimate. Token counts are the runtime's per-agent totals; input/output splits were not exposed.
3. **Self-graded, but deterministically.** The graders are committed scripts run identically on both arms; still, fixtures and graders were authored by the same party running the benchmark.
4. **Arm A's orchestrator did inline work** (T1 build, T2 fix) whose tokens are part of the session rather than separately metered. Arm B's orchestrator also spent unmetered session tokens on more dispatching and two recoveries. The 83.6% figure covers measured worker tokens only.
5. **Small fixtures.** Tasks 4–10 of the plan (auth, migration, refactor, ambiguity, failing deploy, security, persistence) are harder and may narrow or widen the gap.

## Verdict for this slice

On tasks where the work graph does not justify a swarm, the swarm pays ~6× the worker tokens for the same outcome and introduces the only defects observed. The adaptive engine's value is not making the swarm better — it is knowing when not to use it.
