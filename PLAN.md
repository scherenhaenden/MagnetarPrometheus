# Plan of MagnetarPrometheus

This plan captures the project milestones, tasks, estimates, and status. Its structure should remain stable so both humans and tools can track progress consistently.

## Milestones Overview

| Milestone ID | Name | Target Date | Description | Completion Criteria |
| --- | --- | --- | --- | --- |
| `ms-01` | Foundation Setup | 2026-04-02 | Establish repository structure, governance files, and backend/sdk/ui boundaries. | Governance documents exist, project schema exists, and subproject layout is committed. |
| `ms-02` | Core Runtime PoC | 2026-04-12 | Build the first serial workflow engine with models, loader, executor routing, and mock module flow. | A sample workflow runs end-to-end and produces structured context output. |
| `ms-03` | Visual Model Baseline | 2026-04-26 | Define workflow graph schema and UI/editor integration boundary. | Shared schema supports visual nodes and edges, and UI scaffolding can render/edit a sample workflow graph. |

## How To Read This Plan

This plan tracks the currently scoped baseline, not the full long-term product ambition.

Day-specific execution planning should live in `DAY_PLAN.md`, not in this file. `PLAN.md` is for milestones, backlog scope, and durable project-level state.

That distinction matters because the repo now contains a runnable backend slice, but not yet:

- a long-running runtime service
- a job submission API
- a web UI
- a desktop UI
- an operator console

So when this plan says a milestone is `done`, it means the milestone's scoped deliverable is complete, not that MagnetarPrometheus already behaves like the final workflow platform vision.

Execution strategy for upcoming slices:

- prefer user-incremental delivery over large invisible batches
- define work so each round makes one more capability runnable, visible, or inspectable
- when parallelizing, assign disjoint write ownership to avoid collisions between contributors and agents

## Task Backlog

| Task ID | Milestone | Title | Owner | Effort (pts) | Weight (%) | State | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `task-101` | `ms-01` | Establish canonical governance documents | Edward + AI | 3 | 14 | `done` | Initial repository governance baseline created. |
| `task-102` | `ms-01` | Create modular repository layout for backend, sdk, and ui | Edward + AI | 3 | 14 | `done` | Layout added for PyCharm-friendly project root. |
| `task-103` | `ms-02` | Define runtime domain models and workflow schema contracts | Edward | 5 | 24 | `done` | GitHub issue: #1. Includes Python runtime models and shared schema boundary. |
| `task-104` | `ms-02` | Implement workflow loader and serial engine loop | Edward | 5 | 24 | `done` | Based on `PocPlan.md`. Evaluator extracted and next-step resolution hardened. |
| `task-105` | `ms-03` | Design UI graph model for drag-and-drop workflows | Edward + AI | 5 | 24 | `done` | GitHub issue: #7. Defined in `sdk/schemas/workflow-graph-schema.md`. |
| `task-106` | `ms-03` | Define user-visible progress reporting and agile issue/discussion flow | Edward + AI | 3 | 14 | `done` | User-visible progress and GitHub issue/discussion operating rules are documented in the governance files. |
| `task-107` | `ms-02` | Add runnable scripts for backend, tests, and local bootstrap flows | Edward + AI | 3 | 14 | `done` | GitHub issue: #6. The repo must expose simple scripts to run the product and validation flows. |
| `task-108` | `ms-02` | Design Python runtime dependency detection and on-run installation flow | Edward + Jules | 5 | 24 | `done` | GitHub issue: #5. Refined by Jules with structured `BootstrapPolicy` and `BootstrapResult` types. |
| `task-109` | `ms-02` | Enforce 100 percent automated test coverage for core and shared contracts | Edward + AI | 5 | 24 | `done` | GitHub issue: #4. Coverage target is strict and should be automated in the test run path. |
| `task-110` | `ms-01` | Define timestamp-based versioning standard | Edward + AI | 2 | 10 | `done` | GitHub issue: #3. The canonical format is explicitly integrated in backend via a version helper and distinguished from semantic versions. |
| `task-111` | `ms-02` | Create CI pipelines for testing, validation, and release flows | Edward + AI | 5 | 24 | `done` | GitHub issue: #2. CI test workflow exists and release metadata automation has been added. |
| `task-112` | `ms-01` | Define Bitacora retention and archival flow | Edward + AI | 3 | 14 | `planned` | Move `BITACORA.md` entries older than 2 days into durable GitHub surfaces such as Discussions and the wiki so the repo logbook stays current and scannable. |

## Preserved Historical Task Records

These rows are preserved from the merged branch so no prior planning state is deleted during conflict resolution. They should be treated as historical merged records rather than the active source of truth for current task state.

| Historical Task ID | Original Task ID | Milestone | Title | Owner | Effort (pts) | Weight (%) | Historical State | Historical Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `task-103-history-20260326-governance-audit` | `task-103` | `ms-02` | Define runtime domain models and workflow schema contracts | Edward | 5 | 24 | `in_progress` | GitHub issue: #1. Models exist but are oriented mainly around backend needs and not yet shaped for UI graph editing. |
| `task-104-history-20260326-governance-audit` | `task-104` | `ms-02` | Implement workflow loader and serial engine loop | Edward | 5 | 24 | `in_review` | Based on `PocPlan.md`. Workflow loader and engine loop are mostly done, execute a narrow sample workflow, and now include the `email_module` restructuring. |
| `task-105-history-20260326-governance-audit` | `task-105` | `ms-03` | Design UI graph model for drag-and-drop workflows | Edward | 5 | 24 | `planned` | GitHub issue: #7. Must stay aligned with canonical workflow schema. |
| `task-103-history-20260326-runtime-remediation` | `task-103` | `ms-02` | Define runtime domain models and workflow schema contracts | Edward | 5 | 24 | `done` | GitHub issue: #1. Includes Python runtime models and shared schema boundary. |
| `task-104-history-20260326-runtime-remediation` | `task-104` | `ms-02` | Implement workflow loader and serial engine loop | Edward | 5 | 24 | `done` | Based on `PocPlan.md`. Includes restructuring the example module. |
| `task-105-history-20260326-runtime-remediation` | `task-105` | `ms-03` | Design UI graph model for drag-and-drop workflows | Edward + AI | 5 | 24 | `done` | GitHub issue: #7. Must stay aligned with canonical workflow schema. Defined in `sdk/schemas/workflow-graph-schema.md`. |
| `task-110-history-20260326-runtime-remediation` | `task-110` | `ms-01` | Define timestamp-based versioning standard | Edward + AI | 2 | 10 | `done` | GitHub issue: #3. The canonical format is explicitly integrated in backend via a version helper and distinguished from Python package semantic versions. |
| `task-111-history-20260326-runtime-remediation` | `task-111` | `ms-02` | Create CI pipelines for testing, validation, and release flows | Edward + AI | 5 | 24 | `done` | GitHub issue: #2. CI test workflow exists and release metadata automation has been added. |

## Preserved Historical Notes

These notes preserve exact branch-specific wording that would otherwise be lost when two planning stories collide in the same rows.

- `task-104` governance-audit note: `Based on \`PocPlan.md\`. Workflow loader and engine loop are mostly done and execute a narrow sample workflow.`
- `task-104` runtime-remediation note: `Based on \`PocPlan.md\`. Includes restructuring the example module.`
- `task-105` runtime-remediation note: `GitHub issue: #7. Must stay aligned with canonical workflow schema. Defined in \`sdk/schemas/workflow-graph-schema.md\`.`
- `task-110` governance-audit note: `GitHub issue: #3. The canonical format is documented and a release metadata workflow emits the timestamp stamp.`
- `task-110` runtime-remediation note: `GitHub issue: #3. The canonical format is explicitly integrated in backend via a version helper and distinguished from Python package semantic versions.`
- `task-111` governance-audit note: `GitHub issue: #2. CI test pipelines exist, but release automation is only metadata-oriented and lacks a full publication pipeline.`
- `task-111` runtime-remediation note: `GitHub issue: #2. CI test workflow exists and release metadata automation has been added.`
- Governance-audit effort summary: `Completed: 19 pts`, `In review: 5 pts`, `In progress: 15 pts`, `Remaining: 5 pts`
- UI-graph branch effort summary: `Completed: 44 pts`, `In progress: 0 pts`, `Remaining: 0 pts`
- Runtime-remediation effort summary: `Completed: 39 pts`, `In progress: 0 pts`, `Remaining: 5 pts`

## Effort Summary

- Total effort: 44 pts
- Completed: 44 pts
- In progress: 0 pts
- Remaining: 0 pts

## What The Current Baseline Actually Delivers

- A Python proof-of-concept backend runtime.
- A CLI execution path for workflow YAML files.
- A shared SDK/schema layer for workflow contracts.
- An example module and example workflow.
- Local bootstrap, run, and test scripts.
- CI/test/release-metadata automation for the current slice.

## What Still Needs A New Planning Slice

These items are not contradicted by the current `done` state. They simply belong to the next planning baseline rather than the current one.

- Build a long-running backend service or API around the engine.
- Create a first visible UI for running and inspecting workflows.
- Define how jobs/runs are submitted, queued, persisted, and observed.
- Turn the visual graph schema into an actual editable UI surface.
- Clarify the future module lifecycle: discovery, registration, packaging, and execution policies.
- Define a retention policy for `BITACORA.md` so entries older than 2 days are summarized and moved into GitHub Discussions and the repository wiki instead of accumulating indefinitely in the repo root logbook.

## State Definitions

- `planned`: identified but not ready to start
- `ready`: clarified and available for execution
- `in_progress`: actively being worked on
- `in_review`: implementation complete and under review
- `blocked`: cannot proceed due to an active impediment
- `done`: accepted and completed

## Change Management

Update this document whenever task scope or state changes. Reflect the same changes in the relevant project YAML and in [BITACORA.md](/home/edward/Development/MagnetarPrometheus/BITACORA.md).
