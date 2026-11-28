# Roadmap

swarmagents is a skill: markdown instructions an agent runtime executes. Everything the skill text can enforce — adaptive modes, price-aware routing, budgets and checkpoints, typed contracts, run state and resume, project memory, gates — is in [SKILL.md](../skills/swarmagents/SKILL.md) today. The items below need real software, so they are roadmap, not claims:

1. **Observability dashboard** — a live view of the task DAG, active workers, per-worker model/tokens/cost, budget remaining, and verification evidence, plus session replay from the `.swarmagents/runs/` record. Today the per-wave status snapshot and the run-state directory carry this as text.
2. **Durable runtime** — isolated worker processes, worker leases and heartbeats, async callbacks, and crash recovery enforced by a scheduler rather than by instruction-following. Today the skill approximates this with the run-state directory, wave barriers, idempotent-retry rules, and barrier timeouts.
3. **Provider-neutral adapter** — one capability-discovery layer for Claude Code, Codex, Gemini CLI, and direct API or local-model runtimes. Today [`agents/openai.yaml`](../skills/swarmagents/agents/openai.yaml) covers Codex, and the skill documents graceful degradation per missing capability.
4. **Content-hash context cache** — deduplicating transmitted instructions and files by hash instead of by the path-reference convention the skill uses now.
5. **Config validator and interactive setup** — one-command install that validates `.swarmagents.yml`, checks provider rates, and migrates old keys.
6. **Exportable run reports** — the cost table, gate evidence, and recovery history as a shareable artifact generated from run state.
7. **Benchmark campaign** — executing [benchmark-plan.md](benchmark-plan.md) and publishing raw traces.

Standalone module use needs no roadmap: the references are independently readable, and the gates (QA, review, approval) can be adopted without the swarm — point a single agent at [contracts.md](../skills/swarmagents/references/contracts.md) and the gate sections of SKILL.md.

Non-goals, in any phase: more agent personas before benchmarks, routing everything through the strongest model, preloading the repository into every worker, or claiming victory without reproducible evaluations.
