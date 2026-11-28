# Workflow Contracts

Use these contracts as compact coordination records. Prefer repository paths or task artifacts over embedding large source files or logs.

## Blueprint Contract

```yaml
product:
  name: string
  problem: string
  target_users: [string]
  desired_outcomes: [string]
scope:
  in: [string]
  out: [string]
user_journeys:
  - actor: string
    trigger: string
    steps: [string]
    success_state: string
requirements:
  functional: [string]
  non_functional: [string]
  accessibility: [string]
  security_privacy: [string]
architecture:
  existing_stack: [string]
  proposed_changes: [string]
  interfaces: [string]
  data_changes: [string]
  external_dependencies: [string]
execution:
  requested_mode: auto|solo|lean|full
  selected_mode: solo|lean|full
  rationale: string
  independent_work_items: integer
  product_layers: [frontend|backend|database-integration|external-integration|delivery]
  limits:
    max_active_workers: integer
    max_worker_launches: integer
    max_repair_rounds: integer
    token_budget: integer|null
    cost_budget: number|null
acceptance_criteria:
  - id: AC-001
    behavior: string
    verification: string
assumptions: [string]
open_decisions: [string]
delivery:
  required_checks: [string]
  migration_notes: [string]
  rollout_constraints: [string]
```

Do not leave material architecture or product decisions hidden in `assumptions`. Move them to `open_decisions` and resolve them with the user before implementation.

## Work Item Contract

```yaml
task_id: FE-001
title: string
role: product-requirements|frontend|backend|database-integration|tester-qa|code-reviewer|deployment
objective: string
depends_on: [task_id]
wave: integer
inputs: [artifact path or decision ID]
ownership:
  read_scope: [path or glob]
  write_scope: [path or glob]
  interfaces: [API, schema, component, or event]
shared_contracts:
  - name: string
    version: string
    artifact: path
acceptance_criteria: [AC-ID]
expected_artifacts: [path or output]
verification: [command or observable check]
status: ready|active|blocked|review|done
```

Before dispatch, verify that concurrently active work items do not have overlapping write scopes or incompatible interface versions. Broad read scopes are allowed; broad write scopes are not.

## Parallel Wave Manifest

```yaml
wave_id: WAVE-01
objective: string
max_concurrency: integer
mode: solo|lean|full
budget_checkpoint:
  worker_launches_used: integer
  worker_launches_remaining: integer|null
  tokens_used: integer|null
  cost_used: number|null
  status: within-budget|warning|exhausted|unknown
shared_contracts:
  - name: string
    version: string
    artifact: path
ready_tasks: [task_id]
barrier_checks:
  - interface compatibility
  - ownership conflicts
  - focused tests
status: planned|active|integrating|complete|blocked
```

Compute `max_concurrency` from the selected execution mode, task graph, and actual runtime capacity. The smallest of those limits wins. Do not infer that unused runtime slots should be filled.

## Worker Result Contract

```yaml
task_id: string
status: success|warning|error
summary: string
artifacts: [file path, commit, report, or identifier]
changes: [string]
verification:
  commands: [string]
  result: string
blockers: [string]
next_actions: [string]
```

For an error, include the likely root cause, a safe retry path, and an explicit stop condition.

The builder's root-cause hint is evidence, not the recovery decision.

## Agent Cost Ledger Contract

```yaml
agent: string
work_item: task_id
model: string
context_mode: fresh|fork|inherited-default
status: completed|failed|stalled|cancelled
usage_source: measured|estimated|not-reported
tokens:
  input: integer|null
  cached_input: integer|null
  output: integer|null
rates_per_million:
  input: number|null
  cached_input: number|null
  output: number|null
  currency: string
  source: user|provider|unknown
  checked_at: YYYY-MM-DD|null
cost:
  no_cache: number|null
  with_cache: number|null
  estimate_range: [number, number]|null
notes: [string]
```

Use the actual runtime model identifier. Do not infer token counts or rates from the model name. If usage is unavailable, record `not-reported`; a bounded estimate belongs in `estimate_range` and must state its assumptions.

## Manager Recovery Record

```yaml
recovery_id: REC-001
trigger:
  task_id: string
  phase: build|integration|verification|review
  evidence: [artifact path or concise finding]
orchestrator_diagnosis:
  root_cause: unclear-task|incorrect-assumption|interface-mismatch|ownership-conflict|implementation-defect|integration-defect|dependency-environment|product-ambiguity
  reasoning: string
blast_radius:
  affected_tasks: [task_id]
  invalidated_artifacts: [path or identifier]
  affected_contracts: [name and version]
plan_change:
  blueprint_changes: [string]
  contract_changes: [string]
  dependency_changes: [string]
  ownership_changes: [string]
  approach_changes: [string]
repair_tasks: [task_id]
attempt: integer
stop_condition: string
status: diagnosing|replanned|repairing|resolved|needs-user
```

Only the Orchestrator creates or changes this record. Builders may contribute evidence through Worker Results but may not choose the diagnosis, plan change, or retry strategy.

## Verification Report Contract

This is an artifact produced by the Tester/QA coordinator (or builders it enlists for test implementation).

```yaml
status: pass|conditional|fail
acceptance_coverage:
  AC-001: pass|fail|not-run
checks:
  - name: string
    command: string
    result: pass|fail|warning
    evidence: artifact path or concise output
defects:
  - severity: critical|high|medium|low
    reproduction: string
    owner_task: task_id
exceptions: [string]
```

## Review Report Contract

This is an artifact produced by the Code Reviewer, who is never an author of the change under review.

```yaml
status: approve|changes-required
findings:
  - severity: critical|high|medium|low
    area: correctness|security|privacy|accessibility|architecture|performance|testing|operations
    evidence: file path and line, check result, or reproducible behavior
    required_change: string
residual_risks: [string]
```

## Delivery Approval Package

Present this package before asking to push or create a PR:

```yaml
branch: string
remote: string
base_branch: string
commits: [hash and subject]
change_summary: [string]
checks: [name and result]
qa_status: pass|conditional
review_status: approve
execution_mode: solo|lean|full
worker_launches: integer
token_budget_status: within-budget|warning|exhausted|unknown
migrations: [string]
rollout_plan: [string]
rollback_plan: [string]
pr_title: string
pr_body: string
external_actions_pending:
  - push branch to remote
  - create pull request
```

The approval question must name the branch, remote, base branch, and requested external actions. Approval to create a PR does not authorize merging it or deploying it.
