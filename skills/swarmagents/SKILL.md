---
name: swarmagents
description: Coordinate substantial app and website work with one orchestrator and a specialist team of agent groups (product/requirements, frontend, backend, database/integration, QA, code review, deployment), from requirements discovery through an approval-gated pull request and deployment. Use when the user wants a multi-agent delivery team; do not use for small isolated edits that do not benefit from orchestration.
---

# Swarmagents

Act as the sole user-facing orchestrator for a specialist team of worker agents. Clarify the product before implementation, convert the agreed intent into a blueprint and dependency-aware work graph, delegate bounded tasks to the right agent group, integrate and validate the result, and prepare delivery. Keep all external mutations within the user's authorization.

Read [references/contracts.md](references/contracts.md) before producing a blueprint, dispatching implementation work, or preparing a pull request. Read [references/model-routing-and-cost.md](references/model-routing-and-cost.md) before selecting worker models, choosing fresh agents versus inherited forks, or reporting cost. For webpage or site implementation, also read [references/parallel-web-build.md](references/parallel-web-build.md) before staffing builders.

The end-to-end flow is:

`Requirements → Plan → Build Frontend/Backend/Data in parallel → Integrate → Test → Review → Deploy → Verify`

## Execution Mode and Team Model

Choose the execution mode before launching any worker. An explicit user choice or recorded project setting wins. Otherwise choose `auto`, record the selected mode and evidence in the Blueprint, and use the smallest mode that can preserve the required ownership and verification boundaries.

| Mode | Default staffing | Use when | Default limits |
|---|---|---|---|
| **Direct** | Orchestrator only; no workers | A trivial or small isolated edit the user asked for; orchestration would be theater | 0 worker launches; normal repository checks still run |
| **Solo** | Orchestrator, 1 builder, 1 independent verifier | One coherent, independently testable deliverable in one product layer; no material migration, auth, external integration, or irreversible decision | 1 active builder; 2 planned worker launches; 1 repair round |
| **Lean** | Orchestrator, 1–3 builders, 1 QA owner, 1 review owner | Two to four independent work items, usually across one or two layers, with bounded integration | 3 active builders; 5 planned worker launches; 1 repair round |
| **Full** | Orchestrator plus the specialist groups required by the work graph | Five or more independent work items, several product layers, or risk that warrants dedicated requirements, integration, QA, review, or deployment specialists | Runtime capacity and work graph; 2 repair rounds |
| **Persistent** | Full-mode staffing plus the durable run state in "Run State and Resume" | A long-running project expected to span sessions or restarts | Full limits per session; durable run state is mandatory |

Base the choice on evidence recorded in the Blueprint: independent deliverables, product layers touched, risk (migrations, auth, external integrations, irreversible choices), dependency structure, budget, and how much of the work can genuinely run in parallel.

Within Solo, pick one of two execution styles. **Inline:** the Orchestrator implements the fully specified change itself and launches only the independent verifier — the cheapest style that still forbids self-approval. **Fresh-worker:** a builder context implements while the Orchestrator stays managerial — stronger isolation for less-specified work. Record which style was used.

In Solo mode, the same independent verifier may issue two separate artifacts: the Verification Report and Review Report. That keeps both verdicts independent of the author while avoiding a second context for a small change. Lean and Full modes use separate QA and review owners. Product/Requirements and Deployment are conditional roles in every mode: launch them only when their work is substantive. The Orchestrator may prepare a routine delivery package directly; the external-action approval gate never changes.

Before using Solo, confirm that one builder can own the implementation without a broad, ambiguous write scope. Before using Lean, confirm that its builder tasks have genuinely independent deliverables. Select Full when splitting the work creates useful parallelism or independent specialist judgment, not merely because the request sounds ambitious. A one-character edit or similarly trivial change is Direct mode: make it without orchestration artifacts. Select Persistent only when the user describes ongoing work that must survive interruption, not merely a large task.

Do not silently exceed a mode's worker-launch or repair-round limits. First reduce or merge tasks, reuse an existing worker where safe, and prefer deterministic commands over another agent. If completion genuinely requires a higher mode or a user-supplied token/cost ceiling would be exceeded, present the evidence and the revised mode or budget before new dispatches.

| Agent group | Allowed range | Responsibility |
|---|---:|---|
| Orchestrator | 1 (fixed) | Plans work, assigns tasks, manages dependencies, speaks to the user |
| Product/Requirements | 0–3 | Requirements, UX flow, acceptance criteria when the Orchestrator cannot resolve them cheaply |
| Frontend Builders | 0–20 | Pages, components, styling, forms, state, accessibility |
| Backend Builders | 0–20 | APIs, business logic, auth, jobs, observability |
| Database/Integration | 0–20 | Schema, migrations, data access, external APIs, webhooks |
| Tester/QA | 0–3 | Creates and runs unit, API, integration, and E2E tests; Solo uses the independent verifier |
| Code Reviewer | 0–3 | Reviews correctness, security, architecture, and quality; Solo uses the independent verifier |
| Deployment | 0–1 | Builds, deploys, monitors, and rolls back when delivery work warrants a specialist |

**Sizing rule — the Orchestrator chooses every non-fixed count.** For each builder group, derive the count from the work graph: one worker per independently testable, non-overlapping deliverable, bounded by the selected mode, runtime capacity, and a hard cap of 20 active workers per builder group in Full mode. Work beyond the active limit runs in successive waves. Do not split setup, design tokens, documentation, accessibility, or tests into separate workers unless each produces a meaningful deliverable that can be accepted or rejected independently.

The Orchestrator stays at one instance. QA and review may grow to three instances in Full mode when the workload warrants it, but each gate keeps exactly one owner who reconciles helper findings and issues the gate's single verdict. Helpers report to the owner, never to the Orchestrator directly, and never issue verdicts. If multi-agent delegation is unavailable, execute valid work items sequentially within the selected mode and disclose that execution is serial.

This skill is framework-free: the scheduler, worker pools, file isolation, artifact tracking, and quality gates described here must be implemented or enforced by the orchestrator at runtime.

## Model Selection (first run in a project)

Before the first orchestration in a project, check the repository root for `.swarmagents.yml`. If it exists, use the model assignments it records and do not re-ask. If it does not exist — a new project, or the skill's first use — ask the user one batched question: which model should each role run on. Offer the models actually available on the user's platform (inspect the runtime; do not offer models the platform cannot run), grouped by tier, and lead with a recommended mapping they can accept as-is:

| Role | Recommended tier | Why |
|---|---|---|
| Orchestrator | Balanced mid-tier for Solo/Lean; strongest for Full or escalation | Routine scheduling does not always need the highest-cost model; architecture and recovery may |
| Code Review lead | Match model strength to diff risk; strongest for broad or subtle changes | Last quality gate before delivery |
| Product/Requirements | Balanced mid-tier | Structured analysis, not deep reasoning chains |
| Frontend / Backend / Database builders | Balanced mid-tier | Bounded, well-specified tasks; a list to choose from — the user may pick different models per group |
| QA coordinator and helpers | Balanced mid-tier; helpers may drop a tier | Test derivation needs care; execution is mechanical |
| Review helpers | One tier below the lead | Pre-screen findings the lead reconciles |
| Deployment | Balanced mid-tier | Procedural; the approval gate is the safety mechanism, not the model |

Present it as one question with the recommendation first ("accept recommended, or customize per role"), not as eight separate questions. Record the user's choices in `.swarmagents.yml` at the repository root:

```yaml
models:
  orchestrator: string      # model id as the platform names it
  product_requirements: string
  frontend: string
  backend: string
  database_integration: string
  tester_qa: string
  code_reviewer: string
  deployment: string
execution:
  mode: auto  # auto|direct|solo|lean|full|persistent
  optimize_for: balanced  # cost|speed|quality|balanced|budget
  prefer_fresh_workers: true
  allow_inherited_forks: false
  max_active_workers: auto  # mode default unless the user sets a lower cap
  max_worker_launches: auto # mode default unless the user sets a lower cap
  max_repair_rounds: auto   # solo/lean: 1; full: 2
cost_reporting:
  enabled: true
  currency: USD
  token_budget: null
  cost_budget: null
  checkpoints_percent: [50, 80, 100]
  on_budget_exhausted: ask  # ask|hard-stop
  rates: {}  # keyed by actual runtime model id; never guess missing rates
```

Discover the runtime's actual capabilities at intake — subagent support, per-worker model override, usage counters, prompt caching, context limits — rather than assuming them; each documented degradation (serial execution, session-model fallback, `unknown` usage) exists for a capability the runtime may lack. Reuse the file on every later run in that project; apply documented defaults for newly introduced optional keys instead of re-asking. Re-ask only if the user requests a change or a recorded model is no longer available (then re-ask for the affected roles only). If the runtime cannot set a model per worker, say so, run everything on the session's model, and still record the file so the preference applies when the runtime can honor it.

### Context routing and cost

Default to **fresh workers** on their assigned model with a compact written task packet containing the blueprint excerpt, work item, owned files, contract versions, acceptance criteria, reference artifact paths, and verification command. Do not copy the whole parent conversation into every worker.

The full swarm skill and its references belong in the Orchestrator's context. Do not preload them into implementation workers. A worker receives the task packet, the project instructions it actually needs, and referenced files it can read. Return artifact paths and concise findings instead of pasting source files, plans, diffs, or long command output back into the Orchestrator's conversation.

Use an inherited-context fork only when the task depends on context that cannot be made available through a task packet or accessible artifact, such as an attachment the fresh worker cannot inspect. Before forking, record the reason and the expected context/cost tradeoff. If an explicit worker model requires a fresh spawn in the current runtime, the model-routing rule wins: create the task packet and spawn fresh.

When `cost_reporting.enabled` is true, maintain one Agent Cost Ledger record per worker and present the table from `references/model-routing-and-cost.md` at completion. Report measured values when the runtime exposes them. Clearly label estimates, unknown usage, cached-token assumptions, and stalled agents; never invent rates or precision.

Before the first dispatch, give the user a labeled estimate of the run's expected token and cost range alongside the blueprint, anchored to the selected mode and planned launches — an estimate, never presented as a quote. When the runtime exposes token or cost counters, check the configured budget before each new wave and repair dispatch and act on the checkpoints: at 50%, report status; at 80%, stop optional agents, merge remaining compatible work, and use deterministic checks where possible; at 100%, follow `on_budget_exhausted` — stop and ask to continue, or hard-stop with a truthful partial report. `optimize_for` biases the same decisions: `cost` prefers inline/fewer/cheaper workers, `speed` prefers wider waves within limits, `quality` prefers stronger gate models, `budget` treats the ceiling as hard. A budget is not permission to skip required evidence: if the remaining gate cannot be completed within the ceiling, report the exact gap and request a revised budget or scope.

Watch for waste between checkpoints: the same file read repeatedly across workers, reasoning repeated over unchanged inputs, or retries without a changed hypothesis. Fix the task packet, merge tasks, or reuse an existing worker instead of paying for repetition, and terminate a worker that is consuming budget without producing contract-conformant progress.

## Operating Invariants

- The Orchestrator is the only role that speaks to the user and the only role that assigns work. Workers report to it; a worker may not assign work to another worker, change another worker's ownership, or silently revise a shared contract.
- Inspect the repository and available context before asking questions the code can answer.
- Ask at most three concise, decision-relevant questions in one batch. The orchestrator derives, deduplicates, and prioritizes them.
- Do not ask the user to choose implementation details that can be safely inferred. Record reasonable assumptions in the blueprint.
- Do not begin implementation while a missing product decision would materially change architecture, data handling, or acceptance criteria.
- Scale from the number of independent, non-overlapping tasks, never from ambition. Run independent ready tasks concurrently: the active worker count is the smaller of the number of ready tasks and the runtime's available worker slots.
- Apply the selected execution mode's active-worker, total-launch, and repair-round limits before runtime capacity. Record every exception and never expand from Solo or Lean to Full silently.
- When more tasks are ready than the runtime can execute simultaneously, preserve the full plan and execute it in parallel waves rather than discarding tasks or oversubscribing the runtime.
- Each builder owns isolated files or a separate worktree. Concurrent workers must not edit overlapping files; otherwise assign explicit file ownership and serialize conflicts.
- Workers return artifacts, tests, and blockers through the structured contracts in `references/contracts.md` — not just text, and with artifact paths instead of large pasted payloads.
- Every worker launch has a recorded context mode (`fresh`, `fork`, or `inherited-default`) and actual model identifier. Prefer fresh workers with compact task packets to avoid repeatedly billing large parent contexts.
- Workers report results and evidence; they do not diagnose the overall workflow, rewrite the plan, or decide how a failed loop should recover. Those are Orchestrator responsibilities.
- Never place secrets, credentials, or tokens in task packets, contracts, run state, memory, or reports. Reference where a value lives; redact the value itself.
- Deployment is blocked until the Tester/QA and Code Reviewer gates both approve.
- Workers may prepare delivery artifacts but may not push, create a PR, merge, or deploy. A request to build does not authorize those external actions: the Orchestrator owns the user approval boundary, and the authorized executor performs an external action only after the user approves that named action.

## Workflow

### 1. Intake and Reconnaissance

Read the user's task and inspect the repository, instructions, current state, stack, tests, and delivery setup. Summarize the product goal, known constraints, assumptions, and genuine unknowns. If `.swarmagents.yml` is missing, include the Model Selection question in this phase's question batch.

Do not modify product code during this phase unless the user explicitly asked for an immediate small change and orchestration is unnecessary.

### 2. Requirements Conversation

The Orchestrator identifies the users, jobs, scope, priorities, journeys, accessibility needs, integrations, data, security, operational constraints, success measures, and acceptance criteria. In Full mode, or when genuinely different product interpretations need independent analysis, Product/Requirements agents may draft structured findings. Do not launch them merely to restate a clear request. The Orchestrator reconciles any findings and asks the user only the smallest question set needed to proceed.

### 3. Blueprint

Create a blueprint using the reference contract. It must make scope and acceptance testable. Surface it to the user before implementation. If it includes a material assumption, irreversible choice, new external dependency, or scope expansion, ask for confirmation. Otherwise, proceed when the user's original request already authorized implementation.

Store the blueprint in the repository only when documentation changes are within scope. Otherwise keep it in the task record or conversation.

### 4. Work Graph and Staffing

Turn the blueprint into work items with dependencies, ownership boundaries, acceptance criteria, expected artifacts, and verification commands, and route each item to its agent group:

- **Frontend Builders** — partition by page, feature, or component boundary.
- **Backend Builders** — partition by service, endpoint group, or domain capability.
- **Database/Integration** — partition by schema area or external system.
- Reserve integration work for the Orchestrator or a clearly designated integrator.

For a webpage or site, establish shared contracts before parallel implementation: route and page map, design tokens, component boundaries, data types, API schemas, state ownership, and file ownership. Use the decomposition and example task map in `references/parallel-web-build.md`.

Staff within the selected mode. If a layer cannot be safely divided into independently testable write scopes, use one owner there. Count a proposed worker only when its deliverable can be accepted or rejected independently. If multiple approaches are genuinely valuable, use bounded prototypes only when their decision value justifies their extra contexts.

### 5. Parallel Wave Scheduling

The Orchestrator owns the scheduler and remains active while workers run:

1. Build a wave manifest containing only dependency-ready work items, drawn from any group whose dependencies are met — frontend, backend, and data tasks run in parallel when independent.
2. Confirm that write scopes do not overlap and that every shared interface has a versioned contract.
3. Start no more worker instances than the selected mode, work graph, and runtime capacity all permit.
4. Continue useful orchestrator work while agents run: monitor status, answer contract questions, prepare later waves, and report meaningful progress.
5. Collect every result at a wave barrier. Do not integrate a partial interface while sibling tasks are still targeting an older contract.
6. Validate interface compatibility, integrate the wave, run focused checks, and update the work graph.
7. Release newly ready tasks into the next wave. Reassign failed or blocked work only with the failure evidence and a changed recovery plan.

The Orchestrator maintains one source of truth for task state.

When choosing among ready tasks, prioritize the critical path — the dependency chain that bounds total completion time. Merge tiny dependent tasks into one worker context instead of paying a launch for each, and skip parallelism entirely when coordinating two workers would cost more than the time it saves. Treat shared files (registries, barrel files, lockfiles, central configuration) as likely merge conflicts: keep them orchestrator-owned or serialize the tasks that touch them.

### 6. Build and Integrate

Dispatch work items with complete inputs and narrow ownership. Require each worker to return a worker result contract carrying artifacts, tests, and blockers. The Orchestrator reviews results, integrates compatible changes, resolves interface mismatches, and updates the work graph.

When a user changes scope, pause new dispatches, revise the blueprint and affected work items, then resume only valid work.

### 7. Managerial Recovery Loop

The Orchestrator owns recovery whenever implementation, integration, verification, or review fails.

1. **Stop propagation** — pause affected dependent tasks and block delivery. Do not let known-bad artifacts move forward.
2. **Collect evidence** — read the failed work item, worker result, test output, review findings, relevant diff, contract versions, and dependency state.
3. **Diagnose the root cause** — classify it as an unclear task, incorrect assumption, interface mismatch, ownership conflict, implementation defect, integration defect, dependency/environment failure, or product ambiguity.
4. **Determine blast radius** — identify affected artifacts, contracts, tasks, tests, and completed work. Mark stale outputs invalid rather than silently reusing them.
5. **Modify the plan** — revise the blueprint, contract version, task boundary, dependency order, ownership, verification command, or implementation approach as needed.
6. **Issue repair work** — create new bounded assignments with the evidence, changed plan, acceptance criteria, and stop condition. The Orchestrator chooses whether the original or another worker executes them.
7. **Reintegrate and recheck** — run focused verification, then repeat independent review for the affected scope.
8. **Break unproductive loops** — Solo and Lean stop repeat dispatch after one unsuccessful repair round; Full stops after two. The Orchestrator performs a fresh analysis and either changes the plan within the mode or presents evidence for a mode/budget change before another dispatch.

Record each recovery using the Manager Recovery Record in `references/contracts.md`. Ask the user only when recovery requires a product decision, scope change, credentials, external dependency, or new authority. Otherwise the Orchestrator manages the correction autonomously.

### 8. Testing Gate (Tester/QA)

The QA owner derives tests from the blueprint's acceptance criteria and verifies the integrated candidate through escalating tiers: static checks and focused tests first; then the full suite and build; then browser or API integration testing when the product has those surfaces; with security, accessibility, and performance validation added when the change's risk warrants it. Spend the cheaper tier before the costlier one, and record which tiers ran. Every completion claim carries fresh evidence from these runs — a worker's own say-so is never the gate. In Solo mode, the independent verifier owns this verdict; in Lean and Full, the Tester/QA coordinator owns it. The owner may enlist builders for test implementation, but verification of a change is never performed solely by its author.

On any failure, invoke the Managerial Recovery Loop.

The testing gate passes only when required acceptance criteria and repository checks pass, or when the user explicitly accepts a documented exception.

### 9. Code Review Gate

The review owner — never an author of the relevant change — examines the integrated diff and verification report for correctness, scope, security, privacy, accessibility, maintainability, performance, architecture, migrations, rollback risk, and test sufficiency. In Solo mode, the independent verifier issues this as a separate verdict after verification; in Lean and Full, a separate Code Reviewer owns it.

The Orchestrator sends actionable findings through the Managerial Recovery Loop and issues the resulting fix tasks. The gate passes only when no unresolved critical or high-severity issue remains and the blueprint's acceptance criteria are satisfied.

### 10. Delivery, Approval Gate, and Deployment

The Orchestrator prepares a routine delivery package directly. Launch a Deployment agent only when rollout, migration, monitoring, or rollback work is substantial enough to benefit from a specialist. The package includes final status, diff summary, checks, branch name, target remote/base branch, PR title/body, migration notes, rollout plan, and rollback plan. The Orchestrator must ask the user for explicit approval immediately before any push, PR creation, or deploy.

Use a direct approval question that names the exact mutation, for example:

> Approve pushing branch `codex/example` to `origin` and creating a pull request against `main` with the prepared title and description?

Treat silence, ambiguity, or approval of an earlier phase as no approval. Without approval, stop after presenting the prepared delivery package. After approval, the Deployment agent performs only the named action, then monitors the result and stands ready to roll back. Report the outcome truthfully, and do not merge or deploy to production unless that action was separately requested and authorized.

### 11. Post-Deploy Verification

After an approved deploy, the Orchestrator or designated Deployment agent verifies the running system against the blueprint's success measures (health checks, smoke tests, key journeys) and reports the result. A failed verification triggers the rollback plan and the Managerial Recovery Loop.

## Run State and Resume

In Persistent mode — and in any run the user asks to make resumable — keep durable state under `.swarmagents/runs/<run-id>/`: the blueprint, the work graph with task statuses, wave manifests, worker results, recovery records, and the cost ledger. Update it at every wave barrier and gate verdict, not continuously.

On restart or interruption, rebuild from that state instead of replanning: verify that each `done` task's artifacts still exist, re-dispatch only incomplete or invalidated items, and never repeat completed, verified work. Retries are idempotent — before redoing a task, check whether its artifacts already landed. A worker that has produced no result by the time its wave barrier closes is treated as failed with whatever evidence exists, and its task re-enters the graph through the recovery loop. The same directory doubles as a replayable record of the run.

In other modes this directory is optional; the conversation and task records carry the same artifacts.

## Project Memory

A project may keep an optional, plain `.swarmagents/memory.md` recording what future runs keep rediscovering: architectural decisions, accepted conventions, a repository map, recurring failures with the repair that worked, and the stable test and build commands. Update it at completion when a run produced something durable, and note beside each entry the files it depends on; treat an entry as stale once those files change, and verify before reusing it.

Memory is inspectable, versioned with the repository, and deletable. It never overrides the repository's current instructions or code — when they disagree, the repository wins and the memory entry is corrected or removed.

## Progress and Completion

Give the user concise updates at phase boundaries and when a decision, blocker, or material scope change arises. Do not stream internal worker chatter. At each wave barrier, the update is a compact status snapshot: execution mode, active and completed workers with their model and work item, files being modified, retries and recoveries so far, and budget remaining (or `unknown`), plus why any model or mode escalation happened.

Completion requires:

- Blueprint acceptance criteria accounted for.
- Implementation integrated without unresolved ownership conflicts.
- Testing and code-review gates passed or exceptions explicitly accepted.
- Delivery package prepared.
- Agent/model/token/cost table produced when cost reporting is enabled, with measured and estimated values distinguished.
- Push/PR/deploy state reported truthfully: prepared, approved and executed, or withheld pending approval.
