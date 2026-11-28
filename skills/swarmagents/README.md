# Swarmagents

An agent skill that turns one AI coding agent into a full delivery team: a single user-facing **Orchestrator** coordinating specialist agent groups, taking an app or website from requirements discovery through an approval-gated pull request and deploy.

`Requirements → Plan → Build Frontend/Backend/Data in parallel → Integrate → Test → Review → Deploy → Verify`

Use it for substantial app and website work that benefits from parallel builders — not for small isolated edits.

The Orchestrator first chooses a cost-aware mode from the work graph:

| Mode | Team | Best fit |
|---|---|---|
| Direct | Orchestrator only | A trivial isolated edit — no orchestration theater |
| Solo | 1 builder + 1 independent verifier | One coherent deliverable in one product layer |
| Lean | 1–3 builders + QA owner + review owner | Two to four independent work items |
| Full | Specialist groups sized from the graph | Multi-layer or high-risk builds with real parallelism |
| Persistent | Full staffing + durable run state | Long-running projects that must survive restarts |

Solo's verifier issues separate verification and review verdicts, preserving independent judgment without paying for another context — and Solo may run inline, with the Orchestrator implementing and only the verifier launched. Product/Requirements and Deployment are conditional roles in every mode.

## The team

| Agent group | Allowed range | Responsibility |
|---|---:|---|
| Orchestrator | 1 (fixed) | Plans work, assigns tasks, manages dependencies, speaks to the user |
| Product/Requirements | 0–3 | Requirements, UX flow, acceptance criteria when independent analysis is useful |
| Frontend Builders | 0–20 | Pages, components, styling, forms, state, accessibility |
| Backend Builders | 0–20 | APIs, business logic, auth, jobs, observability |
| Database/Integration | 0–20 | Schema, migrations, data access, external APIs, webhooks |
| Tester/QA | 0–3 | Verification owner and optional helpers |
| Code Reviewer | 0–3 | Review owner and optional helpers |
| Deployment | 0–1 | Delivery specialist when rollout work warrants one |

The Orchestrator chooses every non-fixed count from independently testable, non-overlapping deliverables, bounded first by the selected mode and then by runtime capacity. Full mode has a hard cap of 20 active workers per builder group; larger graphs run in waves. It never creates a worker for a task that cannot be independently accepted or rejected. Falls back to serial execution when delegation is unavailable.

**Per-role models and cost reporting.** On its first run in a project the Orchestrator asks which model each role should run on — strongest recommended for the Orchestrator, a tiered list for builders — and saves the choices to `.swarmagents.yml` at the repo root, along with an optimization target (`cost`, `speed`, `quality`, `balanced`, or `budget`). Escalation to a stronger model happens only on recorded evidence that the cheaper one failed. Workers default to fresh contexts with compact task packets instead of expensive full-history forks. Budgets have 50/80/100% checkpoints with a configurable hard-stop or ask-to-continue at exhaustion, a pre-run cost estimate, and a final per-agent model, token, rate, no-cache, and cached-cost table that clearly separates measured usage from estimates. New project, new ask.

**Resumable runs and project memory.** Persistent mode keeps durable run state under `.swarmagents/runs/` — work graph, wave manifests, results, ledger — so an interrupted run resumes without repeating completed, verified work. An optional `.swarmagents/memory.md` carries decisions, conventions, and stable commands between runs; it is plain, versioned, deletable, and never overrides the repository's current instructions.

The full workflow, operating invariants, and quality gates live in [SKILL.md](SKILL.md); the structured handoff contracts in [references/contracts.md](references/contracts.md); the model-routing and cost table in [references/model-routing-and-cost.md](references/model-routing-and-cost.md); and the web-specific wave decomposition in [references/parallel-web-build.md](references/parallel-web-build.md).

## Design notes

The orchestration vocabulary (agents, handoffs, context variables) was popularized by OpenAI Swarm, which has since been superseded by the OpenAI Agents SDK. This skill is standalone and framework-free: the scheduler, worker pools, file isolation, artifact tracking, and quality gates are specified here and enforced by the orchestrating agent at runtime.

## Install

**Claude Code (plugin):**

```
/plugin marketplace add SaiSamardh7/swarmagents
/plugin install swarmagents@swarmagents
```

**Claude Code (manual)** — copy the folder into your skills directory:

```bash
cp -r skills/swarmagents ~/.claude/skills/
```

Then invoke it with `/swarmagents`, or just describe a substantial build.

**Codex** — the `agents/openai.yaml` interface exposes it as `$swarmagents`.
