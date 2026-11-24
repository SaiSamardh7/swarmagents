# Parallel Web Build

Use this reference when the blueprint includes a webpage, website, dashboard, or frontend application. The objective is useful parallelism with deterministic integration, not maximizing agent count.

## Establish Shared Contracts First

Before builders edit code, the orchestrator records:

- Route and page map.
- Design tokens, typography, spacing, color, and responsive breakpoints.
- Page shell and layout slots.
- Component names, props, events, and ownership.
- Client state boundaries and data-loading behavior.
- API request, response, error, and authentication schemas.
- Database entities and migration ownership when relevant.
- Loading, empty, error, permission, and offline states.
- Acceptance criteria and the test responsible for each criterion.

Store these decisions in the blueprint or referenced artifacts. Assign each contract a version. A change to a shared contract invalidates dependent work until the orchestrator updates or reissues it.

## Decompose by Independent Deliverable

For a sufficiently rich page, choose 5-10 independent builder assignments from these boundaries, routed to the matching agent group (Frontend, Backend, Database/Integration, Tester/QA):

1. **Application shell** — routing, navigation, global layout, providers.
2. **Design system** — tokens and reusable primitives, without owning feature sections.
3. **Page section A** — one self-contained content or dashboard region.
4. **Page section B** — a second independent region.
5. **Forms and interactions** — validation, client state, optimistic/error behavior.
6. **Data client** — typed fetchers, caching, adapters, mock fixtures.
7. **Backend/API** — endpoints and domain behavior required by the page.
8. **Database/integration** — schema, queries, migrations, or external service adapter.
9. **Accessibility/responsiveness** — audit and bounded fixes after core structure exists.
10. **Tests** — component, API, integration, or end-to-end coverage against agreed contracts.

Items 1–5 belong to Frontend Builders, 6–7 to Backend Builders, 8 to Database/Integration, 9 to Frontend Builders, and 10 to the Tester/QA coordinator. Merge tiny tasks, omit irrelevant layers, and use fewer workers when boundaries would overlap.

## Recommended Waves

### Wave 0: Contracts and Foundations

Use a small group to establish route/layout structure, design tokens, API/data contracts, and test fixtures. Complete the barrier before feature builders depend on them.

### Wave 1: Independent Features

Launch the largest safe parallel group, typically 5-10 planned tasks across frontend sections, backend endpoints, and data integrations. Every worker receives:

- One work item ID.
- Exact write scope.
- Read-only dependencies.
- Shared contract names and versions.
- Acceptance criteria.
- Verification command.

### Wave 2: Integration and Quality

Integrate shared interfaces, connect sections to real data, resolve responsive and accessibility issues, and complete tests. The Tester/QA coordinator may design tests earlier, but final verification targets the integrated candidate.

## Example Ten-Task Page Plan

```text
FE-01  App shell and route                    writes: app shell/router files
FE-02  Design tokens and UI primitives        writes: design-system files
FE-03  Header and navigation                  writes: header/navigation files
FE-04  Primary page section                   writes: one feature directory
FE-05  Secondary page section                 writes: another feature directory
FE-06  Forms and client interactions          writes: form/state files
FE-07  Typed data client and fixtures          writes: client/fixture files
BE-01  Page API endpoints                     writes: route/service files
DB-01  Schema and data-access layer            writes: migration/repository files
QA-01  Page test suite                         writes: dedicated test files
```

The orchestrator may schedule only the subset whose dependencies are ready. For example, `FE-04` can build against an approved mock contract while `BE-01` and `DB-01` run concurrently, then integration happens at the wave barrier.

## Conflict and Failure Rules

- Never give two active agents the same write scope.
- Shared barrel files, route registries, lockfiles, generated clients, and central configuration belong to the orchestrator/integrator unless explicitly partitioned.
- Builders must not change a shared interface to make their local task easier. They report a contract-change request to the orchestrator.
- On failure, builders preserve evidence and stop; recovery belongs to the Orchestrator (SKILL.md, Managerial Recovery Loop).
- If a worker finishes early, assign only another dependency-ready, non-overlapping task; do not let it self-select work.
