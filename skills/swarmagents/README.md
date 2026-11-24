# Swarmagents

An agent skill that turns one AI coding agent into a full delivery team: a single user-facing **Orchestrator** coordinating specialist agent groups, taking an app or website from requirements discovery through an approval-gated pull request and deploy.

`Requirements → Plan → Build Frontend/Backend/Data in parallel → Integrate → Test → Review → Deploy → Verify`

Use it for substantial app and website work that benefits from parallel builders — not for small isolated edits.

## The team

| Agent group | Count | Responsibility |
|---|---:|---|
| Orchestrator | 1 | Plans work, assigns tasks, manages dependencies, speaks to the user |
| Product/Requirements | 2–3 | Requirements, UX flow, acceptance criteria |
| Frontend Builders | 5–10 | Pages, components, styling, forms, state, accessibility |
| Backend Builders | 5–10 | APIs, business logic, auth, jobs, observability |
| Database/Integration | 5–10 | Schema, migrations, data access, external APIs, webhooks |
| Tester/QA | 1 coordinator | Creates and runs unit, API, integration, and E2E tests |
| Code Reviewer | 1 | Reviews correctness, security, architecture, and quality |
| Deployment | 1 | Builds, deploys, monitors, and rolls back |

Roughly 21–37 agents at full strength; counts are planned capacity, not a quota — the system scales with task size and falls back to serial execution when delegation is unavailable.

The full workflow, operating invariants, and quality gates live in [SKILL.md](SKILL.md); the structured handoff contracts in [references/contracts.md](references/contracts.md); the web-specific wave decomposition in [references/parallel-web-build.md](references/parallel-web-build.md).

## Built on Swarm

The surrounding repo provides the basic `Agent`, tool-calling, handoff, and context-variable mechanisms from OpenAI Swarm. This skill adds what Swarm doesn't have: the scheduler, worker pools, file isolation, artifact tracking, and quality gates.

## Install

**Claude Code** — copy the folder into your skills directory:

```bash
cp -r skills/swarmagents ~/.claude/skills/
```

Then invoke it with `/swarmagents`, or just describe a substantial build.

**Codex** — the `agents/openai.yaml` interface exposes it as `$swarmagents`.
