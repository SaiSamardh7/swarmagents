# Model Routing and Cost Reporting

Use this reference when assigning models, choosing between fresh workers and inherited forks, or reporting usage and estimated API cost.

## Routing Policy

1. Use the configured balanced Orchestrator for Solo and Lean. Use the strongest configured model for Full, material architecture decisions, or recovery escalation. Do not pay the strongest-model rate for routine scheduling by default.
2. Prefer fresh workers on the selected lower-cost model for bounded implementation tasks.
3. Give each fresh worker a compact task packet rather than the whole parent history.
4. Use an inherited fork only when required context cannot be represented by an accessible artifact or concise task packet.
5. Record the actual model and context mode for every launch. Do not assume a requested override was honored without runtime evidence.
6. Keep quality gates independent. A lower-cost review helper may gather findings, but the configured review lead owns the verdict.
7. Do not preload the full swarm skill or its references into workers. The Orchestrator owns orchestration policy; workers receive only their compact task packet and necessary project instructions.
8. Prefer reusing an existing worker for a bounded repair over launching a replacement context when ownership and independence still hold.

Some runtimes require model-overridden agents to start without inherited history. In that case, a complete task packet is mandatory. If a runtime cannot honor the requested worker model, disclose the fallback before presenting cost totals.

## Fresh Worker Task Packet

```yaml
task_id: string
objective: string
blueprint_excerpt: artifact path or concise text
inputs: [artifact path]
ownership:
  read_scope: [path or glob]
  write_scope: [path or glob]
shared_contracts: [name, version, artifact path]
acceptance_criteria: [AC-ID]
reference_assets: [accessible path or identifier]
verification: [command or observable check]
required_result_contract: references/contracts.md#worker-result-contract
```

The packet must be sufficient for the worker to act without the parent's conversational history. If it is not, improve the packet before falling back to a fork.

## Mode-Aware Routing

| Mode | Orchestrator | Builders | Verification and review |
|---|---|---|---|
| Solo | Balanced tier | Balanced or cheaper for a fully specified mechanical task | One independent verifier, balanced by default, issuing separate QA and review verdicts |
| Lean | Balanced tier; escalate only for architecture or recovery | Cheapest tier that is likely to finish without extra turns; balanced is the safe default | Separate balanced QA and review owners; strongest review only for subtle or high-risk diffs |
| Full | Strongest configured tier | Route by task complexity | Dedicated gate owners; helpers may use a lower tier |

Model price alone is not the optimization target. A cheap worker that needs several retries can cost more tokens and time than one balanced worker. Route from task shape, then measure actual turns, input, output, cache usage, and repair count.

## Budget Checkpoints

Before each wave or repair dispatch, record the usage available from the runtime and compare it with `token_budget`, `cost_budget`, and the selected mode's worker-launch limit. At the warning threshold:

1. Cancel optional prototypes, helpers, and duplicate reviews that have not started.
2. Merge compatible remaining work under an existing owner.
3. Use deterministic format, lint, build, and test commands instead of an agent whose only job would be to run them.
4. Preserve the independent gate required by the selected mode.

If usage is not reported, the launch and repair limits remain enforceable proxies. Mark token and cost status `unknown`; do not pretend the budget was verified.

## Required Cost Table

Use this format for the final per-agent breakdown:

| Agent | Model | Rates (in/out per M) | Tokens (in / out) | No-cache est. | With caching est. |
|---|---|---:|---:|---:|---:|
| Orchestrator | actual model | current rates or `unknown` | measured or clearly estimated | value or `unknown` | value or `unknown` |
| Worker / work item | actual model and context mode | current rates or `unknown` | measured or clearly estimated | value or `unknown` | value or `unknown` |
| **Total** |  |  | measured total plus labeled estimates | range or value | range or value |

Add concise notes below the table covering:

- Which agents used a different model.
- Which workers were fresh versus inherited forks and why.
- Stalled or cancelled agents whose usage was not reported.
- Whether token splits are measured or estimated and the uncertainty used.
- A cheaper alternative routing when it would materially reduce cost without unacceptable quality loss.

## Cost Rules

- Never hard-code example model names or rates as if they are available in the current runtime.
- Use rates supplied by the user or verified from the current provider. Record the rate source and check date.
- `No-cache cost = input_tokens × input_rate + output_tokens × output_rate`, with token counts and rates normalized per million.
- Compute cached cost only when cached-token counts and a cached-input rate are known. Otherwise report `unknown` or a labeled range with the assumption.
- If the runtime reports only total tokens, do not present an exact input/output split. Use an explicitly labeled estimate and show an uncertainty range.
- For stalled agents with no usage report, show `not reported`. A bounded upper estimate is allowed only when based on known context and output limits.
- Do not combine measured and estimated numbers into a deceptively precise total. Prefer a range and explain what anchors it.

## Comparison Scenario

When inherited forks dominate cost, compare the actual routing with this alternative:

`Strong Orchestrator + fresh lower-cost workers + written task packets`

State the estimated savings and the quality tradeoff. For visual or attachment-driven work, the task packet should include an accessible image path, structured visual specification, or both. If the worker cannot access the reference, say so instead of claiming equivalence.
