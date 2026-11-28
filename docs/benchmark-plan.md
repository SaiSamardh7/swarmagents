# Benchmark Plan

A "works better" claim needs evidence. This is the preregistered plan for benchmarking swarmagents against comparable orchestration setups (see the [competitive comparison](competitive-comparison-2026-11-27.md)) on identical tasks. The full ten-task suite has been executed against an unconditional-swarm baseline — results in [benchmark-results-2026-11-27-slice.md](benchmark-results-2026-11-27-slice.md); the cross-tool campaign has not run, so the README makes no universal-winner claim.

## Task Suite

Each system runs the same ten tasks from the same starting repositories:

1. Single landing page.
2. Small bug fix.
3. Cross-layer feature (frontend + backend + data).
4. Authentication integration.
5. Database migration.
6. Large refactor.
7. Ambiguous product request (requirements discovery required).
8. Failing deployment to diagnose and repair.
9. Security-sensitive change.
10. Long-running project resumed after interruption.

## Metrics

Per task, record:

- Task success rate (acceptance criteria met without human repair).
- Human corrections required.
- Input/output tokens (cached input separated when metered).
- Actual dollar cost at the provider's published rates.
- Wall-clock completion time.
- Tests passing at completion.
- Defects introduced (found by an independent reviewer after completion).
- Context duplication (same content transmitted to multiple workers).
- Worker launches (and how many were unnecessary in hindsight).
- Recovery success after induced failure or interruption.
- Quality of final documentation and delivery package.

Publish raw traces and the exact configuration (models, rates, `.swarmagents.yml`) for every run so results are reproducible.

## Targets

The configuration is tuned against these targets, not against vibes:

- ≥ 90% task completion on the suite.
- 40–60% lower cost than unconditional Full-mode execution on the same tasks.
- < 5% unnecessary worker launches.
- ≥ 95% adherence to user budgets.
- Zero unapproved external or destructive actions.
- Solo-mode webpage builds typically below 200k tokens.
- Interrupted Persistent runs resume without repeating completed, verified work.

## Relation to `evals/`

The free structure tests and the scenario evals in [`evals/`](../evals/) probe the invariants (approval gate, no self-review, disclosure, mode selection) and run in CI. This benchmark suite is the paid, cross-system complement; it runs manually and its spend is approved before each campaign.
