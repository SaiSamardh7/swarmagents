# swarmagents

One skill that turns your coding agent into a delivery team — with the safety rails most multi-agent setups skip.

`/swarmagents` runs a single user-facing **Orchestrator** that staffs specialist agent groups — product/requirements, frontend, backend, database/integration, QA, code review, deployment — and takes an app or website from requirements discovery to an **approval-gated** pull request and deploy.

`Requirements → Plan → Build Frontend/Backend/Data in parallel → Integrate → Test → Review → Deploy → Verify`

## Why this one

Most multi-agent skills sell the swarm. This one is built around the **gates**:

- **No self-review.** A change is never verified solely by its author; the Tester/QA and Code Reviewer gates must both pass before delivery.
- **No silent mutations.** Workers may prepare a branch, PR text, or deploy plan, but only the user's explicit approval of the *named action* ("push branch X and open a PR against main?") lets it execute.
- **Managerial recovery, not retry spam.** Failures trigger an evidence-collecting recovery loop with root-cause classification and blast-radius analysis; the same root cause surviving two repair cycles halts dispatch and forces a changed plan.
- **Collision-free parallelism.** Versioned handoff contracts, explicit file ownership, and wave scheduling keep 5–10 parallel builders per layer from stepping on each other — and the system falls back to serial execution when delegation is unavailable.

The full workflow and operating invariants live in [SKILL.md](skills/swarmagents/SKILL.md), the structured handoff contracts in [references/contracts.md](skills/swarmagents/references/contracts.md), and the web-specific wave decomposition in [references/parallel-web-build.md](skills/swarmagents/references/parallel-web-build.md).

## Install

**Claude Code (plugin):**

```
/plugin marketplace add SaiSamardh7/swarmagents
/plugin install swarmagents@swarmagents
```

**Claude Code (manual):**

```bash
cp -r skills/swarmagents ~/.claude/skills/
```

Then invoke it with `/swarmagents`, or just describe a substantial build.

**Codex:** [`agents/openai.yaml`](skills/swarmagents/agents/openai.yaml) exposes it as `$swarmagents`.

## Scope

Use it for substantial app and website work that benefits from parallel builders. It deliberately refuses to orchestrate small isolated edits — a team is overhead when one agent suffices. Team counts (roughly 21–37 agents at full strength) are planned capacity, not a quota; the orchestrator staffs the smallest useful pool for the work graph.

## Security model

Skills are instructions your agent follows, so authorization boundaries matter. This skill's invariants keep every external mutation (push, PR, merge, deploy) behind an explicit, per-action user approval, and workers can never grant themselves authority. Details in [SECURITY.md](SECURITY.md).

## License

[MIT](LICENSE)
