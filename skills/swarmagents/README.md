# Swarmagents

An agent skill that turns one AI coding agent into a full delivery team: a single user-facing **Orchestrator** coordinating specialist agent groups, taking an app or website from requirements discovery through an approval-gated pull request and deploy.

`Requirements → Plan → Build Frontend/Backend/Data in parallel → Integrate → Test → Review → Deploy → Verify`

Use it for substantial app and website work that benefits from parallel builders — not for small isolated edits.

## The team

| Agent group | Typical (mid-size app) | Responsibility |
|---|---:|---|
| Orchestrator | 1 (fixed) | Plans work, assigns tasks, manages dependencies, speaks to the user |
| Product/Requirements | 2–3 | Requirements, UX flow, acceptance criteria |
| Frontend Builders | 5–10 | Pages, components, styling, forms, state, accessibility |
| Backend Builders | 5–10 | APIs, business logic, auth, jobs, observability |
| Database/Integration | 5–10 | Schema, migrations, data access, external APIs, webhooks |
| Tester/QA | 1 coordinator (fixed) | Creates and runs unit, API, integration, and E2E tests |
| Code Reviewer | 1 (fixed) | Reviews correctness, security, architecture, and quality |
| Deployment | 1 (fixed) | Builds, deploys, monitors, and rolls back |

The Orchestrator chooses every non-fixed count from the work graph — one worker per independent, non-overlapping write scope, bounded only by runtime capacity. The typical values describe a mid-size app, not a limit; the fixed roles stay singular to keep one source of truth per gate. Falls back to serial execution when delegation is unavailable.

The full workflow, operating invariants, and quality gates live in [SKILL.md](SKILL.md); the structured handoff contracts in [references/contracts.md](references/contracts.md); the web-specific wave decomposition in [references/parallel-web-build.md](references/parallel-web-build.md).

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
