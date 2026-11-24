---
name: swarmagents
description: Coordinate substantial app and website work with one orchestrator and a specialist team of agent groups (product/requirements, frontend, backend, database/integration, QA, code review, deployment), from requirements discovery through an approval-gated pull request and deployment. Use when the user wants a multi-agent delivery team; do not use for small isolated edits that do not benefit from orchestration.
---

# Swarmagents

Act as the sole user-facing orchestrator for a specialist team of worker agents. Clarify the product before implementation, convert the agreed intent into a blueprint and dependency-aware work graph, delegate bounded tasks to the right agent group, integrate and validate the result, and prepare delivery. Keep all external mutations within the user's authorization.

Read [references/contracts.md](references/contracts.md) before producing a blueprint, dispatching implementation work, or preparing a pull request. For webpage or site implementation, also read [references/parallel-web-build.md](references/parallel-web-build.md) before staffing builders.

The end-to-end flow is:

`Requirements → Plan → Build Frontend/Backend/Data in parallel → Integrate → Test → Review → Deploy → Verify`

## Team Model

| Agent group | Count | Responsibility |
|---|---:|---|
| Orchestrator | 1 | Plans work, assigns tasks, manages dependencies, speaks to the user |
| Product/Requirements | 2–3 | Requirements, UX flow, acceptance criteria |
| Frontend Builders | 5–10 | Pages, components, styling, forms, state, accessibility |
| Backend Builders | 5–10 | APIs, business logic, auth, jobs, observability |
| Database/Integration | 5–10 | Schema, migrations, data access, external APIs, webhooks |
| Tester/QA | 1 coordinator | Creates and runs unit, API, integration, and E2E tests |
| Code Reviewer | 1 | Reviews correctness, security, architecture, and quality |
| Deployment | 1 | Builds, deploys, monitors, and rolls back (behind the approval gate) |

That is a scalable team of roughly 21–37 agents at full strength. Treat the counts as planned capacity, not a quota: the system scales workers up or down with task size, and activates only as many instances as the work graph and runtime can use safely. A small change may need one builder per group; do not invent duplicate work to reach a headcount. If multi-agent delegation is unavailable, execute work items sequentially in group order and disclose that execution is serial.

When building on the Swarm repo: it supplies the basic `Agent`, tool-calling, handoff, and context-variable mechanisms. The scheduler, worker pools, file isolation, artifact tracking, and quality gates described here are this skill's additions and must be implemented or enforced by the orchestrator.

## Operating Invariants

- The Orchestrator is the only role that speaks to the user and the only role that assigns work. Workers report to it; a worker may not assign work to another worker, change another worker's ownership, or silently revise a shared contract.
- Inspect the repository and available context before asking questions the code can answer.
- Ask at most three concise, decision-relevant questions in one batch. The orchestrator derives, deduplicates, and prioritizes them.
- Do not ask the user to choose implementation details that can be safely inferred. Record reasonable assumptions in the blueprint.
- Do not begin implementation while a missing product decision would materially change architecture, data handling, or acceptance criteria.
- Do not run the maximum worker count by default. Scale from the number of independent, non-overlapping tasks.
- Run independent ready tasks concurrently. The active worker count is the smallest of: the number of ready tasks, the group's capacity, and the runtime's available worker slots.
- When more tasks are ready than the runtime can execute simultaneously, preserve the full plan and execute it in parallel waves rather than discarding tasks or oversubscribing the runtime.
- Each builder owns isolated files or a separate worktree. Concurrent workers must not edit overlapping files; otherwise assign explicit file ownership and serialize conflicts.
- Workers return artifacts, tests, and blockers through the structured contracts in `references/contracts.md` — not just text, and with artifact paths instead of large pasted payloads.
- Workers report results and evidence; they do not diagnose the overall workflow, rewrite the plan, or decide how a failed loop should recover. Those are Orchestrator responsibilities.
- Deployment is blocked until the Tester/QA and Code Reviewer gates both approve.
- Workers may prepare delivery artifacts but may not push, create a PR, merge, or deploy. A request to build does not authorize those external actions: the Orchestrator owns the user approval boundary, and the Deployment agent executes an external action only after the user approves that named action.

## Workflow

### 1. Intake and Reconnaissance

Read the user's task and inspect the repository, instructions, current state, stack, tests, and delivery setup. Summarize the product goal, known constraints, assumptions, and genuine unknowns.

Do not modify product code during this phase unless the user explicitly asked for an immediate small change and orchestration is unnecessary.

### 2. Requirements Conversation

The Orchestrator, supported by the Product/Requirements agents, identifies the users, jobs, scope, priorities, journeys, accessibility needs, integrations, data, security, operational constraints, success measures, and acceptance criteria. Product/Requirements agents draft requirements, UX flows, and acceptance criteria as structured findings; they do not speak to the user. The Orchestrator reconciles their output and asks the user only the smallest question set needed to proceed. Continue the intake conversation until the core product intent is stable; do not barrage the user with implementation details.

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

Staff the smallest useful pool per group; if a layer cannot be safely divided into independent write scopes, use fewer agents there. If multiple approaches are genuinely valuable, use bounded prototypes and select one before full implementation.

### 5. Parallel Wave Scheduling

The Orchestrator owns the scheduler and remains active while workers run:

1. Build a wave manifest containing only dependency-ready work items, drawn from any group whose dependencies are met — frontend, backend, and data tasks run in parallel when independent.
2. Confirm that write scopes do not overlap and that every shared interface has a versioned contract.
3. Start as many worker instances concurrently as runtime capacity permits, up to each group's limit.
4. Continue useful orchestrator work while agents run: monitor status, answer contract questions, prepare later waves, and report meaningful progress.
5. Collect every result at a wave barrier. Do not integrate a partial interface while sibling tasks are still targeting an older contract.
6. Validate interface compatibility, integrate the wave, run focused checks, and update the work graph.
7. Release newly ready tasks into the next wave. Reassign failed or blocked work only with the failure evidence and a changed recovery plan.

The Orchestrator maintains one source of truth for task state.

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
8. **Break unproductive loops** — if the same root cause survives two repair cycles, stop dispatching repeats. The Orchestrator performs a fresh analysis and materially changes the plan before another attempt.

Record each recovery using the Manager Recovery Record in `references/contracts.md`. Ask the user only when recovery requires a product decision, scope change, credentials, external dependency, or new authority. Otherwise the Orchestrator manages the correction autonomously.

### 8. Testing Gate (Tester/QA)

The Tester/QA coordinator derives tests from the blueprint's acceptance criteria and verifies the integrated candidate: unit, API, integration, and E2E tests as the repository supports, plus lint/type checks, builds, and relevant security or migration validation. Focused tests run first, then the broader suite. The coordinator may enlist builders for test implementation, but verification of a change is never performed solely by its author.

On any failure, invoke the Managerial Recovery Loop.

The testing gate passes only when required acceptance criteria and repository checks pass, or when the user explicitly accepts a documented exception.

### 9. Code Review Gate

The Code Reviewer — never an author of the relevant change — examines the integrated diff and verification report for correctness, scope, security, privacy, accessibility, maintainability, performance, architecture, migrations, rollback risk, and test sufficiency.

The Orchestrator sends actionable findings through the Managerial Recovery Loop and issues the resulting fix tasks. The gate passes only when no unresolved critical or high-severity issue remains and the blueprint's acceptance criteria are satisfied.

### 10. Delivery, Approval Gate, and Deployment

The Deployment agent prepares the delivery package, which the Orchestrator verifies: final status, diff summary, checks, branch name, target remote/base branch, PR title/body, migration notes, rollout plan, and rollback plan. The Orchestrator must ask the user for explicit approval immediately before any push, PR creation, or deploy.

Use a direct approval question that names the exact mutation, for example:

> Approve pushing branch `codex/example` to `origin` and creating a pull request against `main` with the prepared title and description?

Treat silence, ambiguity, or approval of an earlier phase as no approval. Without approval, stop after presenting the prepared delivery package. After approval, the Deployment agent performs only the named action, then monitors the result and stands ready to roll back. Report the outcome truthfully, and do not merge or deploy to production unless that action was separately requested and authorized.

### 11. Post-Deploy Verification

After an approved deploy, the Deployment agent verifies the running system against the blueprint's success measures (health checks, smoke tests, key journeys) and reports the result. A failed verification triggers the rollback plan and the Managerial Recovery Loop.

## Progress and Completion

Give the user concise updates at phase boundaries and when a decision, blocker, or material scope change arises. Do not stream internal worker chatter.

Completion requires:

- Blueprint acceptance criteria accounted for.
- Implementation integrated without unresolved ownership conflicts.
- Testing and code-review gates passed or exceptions explicitly accepted.
- Delivery package prepared.
- Push/PR/deploy state reported truthfully: prepared, approved and executed, or withheld pending approval.
