# Swarmagents Competitive Comparison

*Generated: 2026-11-27 | Confidence: high for documented behavior; medium for real-world quality and cost*

## Executive summary

No repository is universally better. For a small webpage, Superpowers' inline execution or individual gstack skills are likely cheaper and simpler than a full swarm. Oh My Claude Code (OMC) provides the strongest packaged multi-agent user experience and observability. Ruflo and AWS CLI Agent Orchestrator (CAO) provide substantially more runtime infrastructure. Swarmagents has the clearest documented governance model of this set: versioned handoff contracts, explicit ownership, independent QA/review verdicts, managerial recovery, and a named user-approval boundary before external mutations.

The main weakness in swarmagents was that its visible staffing examples encouraged full-team ceremony for work that did not justify it. The new Solo, Lean, and Full modes address that gap while retaining Full mode's strict guarantees.

## Comparison matrix

| Project | Primary shape | Cost control | Multi-agent runtime | Quality/governance | Best fit |
|---|---|---|---|---|---|
| **swarmagents** | One portable delivery skill | Mode limits, compact fresh-worker packets, budgets, per-agent ledger | Uses the host's delegation tools; no bundled runtime | Versioned contracts, file ownership, QA/review gates, recovery records, approval gate | Governed app/site delivery where auditability matters |
| **gstack** | Large suite of independent role skills and supporting binaries | Invoke only the phase needed; context/spend tooling; lean/full review paths | Optional crew/factory tooling rather than one required swarm runtime | Strong review, QA, ship, security, and evidence workflows | Founders and teams wanting a broad engineering operating system |
| **OMC** | Claude Code plugin with modes, hooks, agents, state, HUD, and provider routing | Solo/team execution, tiered models, cycle caps, observability | Built-in team orchestration and external CLI workers | Multi-phase QA and parallel validation with persistent state | Turnkey Claude Code multi-agent automation |
| **Superpowers** | Composable development methodology expressed as skills | Explicit cheap inline path versus fresh-agent-per-task path | Uses native subagents; little runtime infrastructure | TDD, plan discipline, per-task review, final verification | Small-to-medium implementation work with rigorous engineering habits |
| **Ruflo** | Full agent meta-harness and plugin ecosystem | Cost-tracker plugin, model routing, bounded context delegation | Swarms, memory, MCP, hooks, federation, learning, background workers | Broad security, memory, and verification capabilities | Large-scale agent platforms and persistent organizational memory |
| **AWS CAO** | Local supervisor/worker runtime for many coding CLIs | Explicit do-or-delegate heuristic; provider/model overrides | Isolated terminal processes, async assign, sync handoff, durable workflows | Strong process isolation, callbacks, approvals, and workflow validation | Multi-provider orchestration and durable operational workflows |

## Project-by-project findings

### gstack

gstack is a broad engineering workflow suite. Its sprint is organized as Think → Plan → Build → Review → Test → Ship → Reflect, but each specialist skill can be invoked independently. Its documentation is unusually candid: a November 2026 evaluation reported no improvement in ordinary bug-fix success from merely having gstack installed, so it positions its value in workflow, review, shipping, and safety rather than raw model intelligence. It also contains dedicated context/spend tooling and both lean and fuller review paths. Sources: [README](https://github.com/garrytan/gstack/blob/main/README.md), [autoplan skill](https://github.com/garrytan/gstack/blob/main/autoplan/SKILL.md), [architecture](https://github.com/garrytan/gstack/blob/main/ARCHITECTURE.md).

**Where gstack is better:** breadth, installation/host support, tooling depth, real browser QA, release automation, documentation, and evaluation infrastructure.

**Where swarmagents is better:** it presents one smaller, coherent contract for multi-agent delivery. File ownership, versioned interfaces, wave barriers, manager-owned recovery, and named external-action approval are easier to inspect in one place.

**Verdict:** gstack is the better general engineering toolkit. Swarmagents is the better focused specification when a team needs explicit multi-agent responsibilities and audit records.

### Oh My Claude Code

OMC is the closest functional competitor. It has explicit Team and Autopilot modes, a staged team pipeline, tiered agent/model routing, state persistence, replay logs, a HUD, intervention thresholds, QA cycles, and parallel architecture/security/code-quality validation. Its Autopilot configuration can execute solo or through a team and caps QA and validation cycles. Sources: [README](https://github.com/Yeachan-Heo/oh-my-claudecode/blob/main/README.md), [Autopilot skill](https://github.com/Yeachan-Heo/oh-my-claudecode/blob/main/skills/autopilot/SKILL.md), [performance monitoring](https://github.com/Yeachan-Heo/oh-my-claudecode/blob/main/docs/PERFORMANCE-MONITORING.md), [model compatibility](https://github.com/Yeachan-Heo/oh-my-claudecode/blob/main/docs/agents/model-compatibility.md).

**Where OMC is better:** turnkey user experience, persistent execution, runtime observability, provider routing, agent lifecycle tracking, session replay, and automatic interventions.

**Where swarmagents is better:** much smaller surface area, fewer runtime dependencies, clearer framework independence, simpler trust model, and a more explicit approval boundary for push/PR/deploy actions.

**Verdict:** OMC is better for users who want a complete Claude Code automation product. Swarmagents is better for teams that want a portable, reviewable governance protocol without installing a large runtime.

### Superpowers

Superpowers offers the clearest cost/quality choice. Subagent-driven development uses a fresh implementer and reviewer per task, while executing-plans keeps implementation in one context and uses one fresh final reviewer. Its planning rules emphasize independently testable tasks rather than arbitrary task counts, and its verification skill requires fresh command evidence before completion claims. Sources: [README](https://github.com/obra/superpowers/blob/main/README.md), [subagent-driven development](https://github.com/obra/superpowers/blob/main/skills/subagent-driven-development/SKILL.md), [executing plans](https://github.com/obra/superpowers/blob/main/skills/executing-plans/SKILL.md), [writing plans](https://github.com/obra/superpowers/blob/main/skills/writing-plans/SKILL.md), [verification](https://github.com/obra/superpowers/blob/main/skills/verification-before-completion/SKILL.md).

**Where Superpowers is better:** simplicity, TDD discipline, right-sized tasks, a plainly documented cheapest path, and broad applicability to normal coding work.

**Where swarmagents is better:** multi-layer work graphs, parallel waves, versioned shared interfaces, specialist group ownership, formal recovery, and delivery approval packaging.

**Verdict:** Superpowers is likely better for most small and medium coding tasks and for a single webpage. Swarmagents becomes better when several agents must coordinate against shared contracts and delivery must be independently gated.

### Ruflo

Ruflo is a full meta-harness: MCP tools, hooks, more than one hundred agent definitions, vector memory, learning, swarms, background workers, federation, security plugins, and cost tracking. Its bounded-context benchmark is careful about an important distinction: coordinator payload fell about 97.6% in a deterministic fixture, but total boundary bytes increased about 3.8%, and the project explicitly declines to claim billed savings without a live provider pilot. Sources: [README](https://github.com/ruvnet/ruflo/blob/main/README.md), [root skill](https://github.com/ruvnet/ruflo/blob/main/SKILL.md), [swarm orchestration skill](https://github.com/ruvnet/ruflo/blob/main/.agents/skills/swarm-orchestration/SKILL.md), [context delegation benchmark](https://github.com/ruvnet/ruflo/blob/main/docs/benchmarks/context-delegation.md), [framework comparison](https://github.com/ruvnet/ruflo/blob/main/docs/compare.md).

**Where Ruflo is better:** persistent memory, learning, federation, runtime scale, plugin breadth, observability, and infrastructure for long-lived agent systems.

**Where swarmagents is better:** install and cognitive simplicity, a much smaller attack/configuration surface, direct traceability from requirements to delivery, and suitability for a single repository without operating an agent platform.

**Verdict:** Ruflo is better as an agent platform. Swarmagents is better as a comprehensible delivery protocol for a coding session or project.

### AWS CLI Agent Orchestrator

CAO provides real supervisor/worker processes across Claude Code, Codex, Kiro, and other CLIs. It separates synchronous handoff from asynchronous assignment, supports callback guarantees and durable scripted workflows, and explicitly warns that delegation has a fixed startup and verification cost. Its documentation gives a measured example where a small dependency-floor edit was faster when done directly than when delegated. Sources: [README](https://github.com/awslabs/cli-agent-orchestrator/blob/main/README.md), [supervisor protocols](https://github.com/awslabs/cli-agent-orchestrator/blob/main/agent-plugin/cao/skills/cao-supervisor-protocols/SKILL.md), [agent routing](https://github.com/awslabs/cli-agent-orchestrator/blob/main/agent-plugin/cao/skills/cao-agent-routing/SKILL.md), [workflows](https://github.com/awslabs/cli-agent-orchestrator/blob/main/docs/workflows.md), [orchestration patterns](https://github.com/awslabs/cli-agent-orchestrator/blob/main/docusaurus/docs/core-concepts/orchestration-patterns.md).

**Where CAO is better:** process isolation, provider independence, reliable callbacks, durable workflow execution, remote/fleet management, and operational tooling.

**Where swarmagents is better:** product-development semantics. CAO supplies orchestration primitives; swarmagents supplies the requirements, ownership, integration, QA, review, recovery, and approval policy those primitives can execute.

**Verdict:** CAO is a stronger execution runtime. Swarmagents is a stronger ready-made app/site delivery policy. They are complementary rather than direct substitutes.

## Which is better by use case?

| Use case | Best choice | Why |
|---|---|---|
| One webpage or bounded feature | **Superpowers**, then gstack | Lowest ceremony with independent final review and strong verification |
| Broad founder/product workflow | **gstack** | Deep product, design, QA, release, and operating-tool coverage |
| Turnkey Claude Code multi-agent automation | **OMC** | Modes, routing, persistence, HUD, replay, and lifecycle management |
| Large persistent agent platform | **Ruflo** | Memory, learning, federation, plugins, and background infrastructure |
| Multi-provider isolated worker runtime | **AWS CAO** | Real CLI processes, handoff/assign semantics, callbacks, and workflows |
| Auditable governed app/site delivery | **swarmagents** | Most explicit compact contract for ownership, gates, recovery, and user approval |

## Changes adopted in swarmagents

1. Added evidence-based Solo, Lean, and Full execution modes.
2. Made Product/Requirements and Deployment conditional roles.
3. Added per-mode active-worker, total-launch, and repair-round limits.
4. Added token and cost budgets with an 80% warning checkpoint.
5. Changed Solo to one builder plus one independent verifier that issues separate QA and review verdicts.
6. Removed the `5–10`-builder target from webpage decomposition.
7. Changed routine Solo/Lean orchestration to a balanced model tier, reserving the strongest tier for Full mode, architecture, and recovery escalation.
8. Prohibited preloading the full swarm skill into implementation workers.
9. Added a cost-aware mode-selection eval and free structural checks.

## Methodology and limitations

The comparison inspected each repository's primary README and the documentation most directly related to orchestration, execution modes, model routing, context, verification, review, and workflows on 2026-11-27. Repository documentation is authoritative for intended behavior but does not prove real-world quality. Star counts were used only to understand adoption and were not used to select a winner. No paid head-to-head implementation benchmark was run, so cost and quality conclusions are architectural inferences unless a project supplied a bounded measurement; those measurements are described with their stated limitations.
