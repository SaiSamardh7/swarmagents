# Security

swarmagents is an agent skill — plain instructions your coding agent follows. It ships no executable code, so the security surface is the authority it tells your agent to exercise.

## Authorization model

The skill's operating invariants are designed to keep the agent inside the user's authorization:

- **Explicit, per-action approval for external mutations.** Pushing a branch, creating a PR, merging, or deploying each requires the user to approve that named action immediately beforehand. Silence, ambiguity, or approval of an earlier phase is treated as no approval.
- **Workers hold no external authority.** Builder, QA, review, and deployment agents may prepare artifacts but may not push, open PRs, merge, or deploy; only the user's approval routed through the orchestrator releases an action.
- **No self-verification.** A change is never verified solely by its author, and deployment is blocked until the independent QA and code-review gates pass.
- **Bounded recovery.** Failure handling collects evidence and revises the plan; it never escalates authority to retry around a gate.

## Prompt injection

Content the agent reads while working (repository files, web pages, tool output) is data, not instructions. Nothing a worker reads can approve an external mutation — approval must come from the user in conversation.

## Reporting

If you find a way this skill's instructions can lead an agent to exceed user authorization, please open a GitHub issue (or a private security advisory on this repository) describing the scenario.
