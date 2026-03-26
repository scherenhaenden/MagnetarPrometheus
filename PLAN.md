# Plan of MagnetarPrometheus

This plan captures the project milestones, tasks, estimates, and status. Its structure should remain stable so both humans and tools can track progress consistently.

## Milestones Overview

| Milestone ID | Name | Target Date | Description | Completion Criteria |
| --- | --- | --- | --- | --- |
| `ms-01` | Foundation Setup | 2026-04-02 | Establish repository structure, governance files, and backend/sdk/ui boundaries. | Governance documents exist, project schema exists, and subproject layout is committed. |
| `ms-02` | Core Runtime PoC | 2026-04-12 | Build the first serial workflow engine with models, loader, executor routing, and mock module flow. | A sample workflow runs end-to-end and produces structured context output. |
| `ms-03` | Visual Model Baseline | 2026-04-26 | Define workflow graph schema and UI/editor integration boundary. | Shared schema supports visual nodes and edges, and UI scaffolding can render/edit a sample workflow graph. |

## Task Backlog

| Task ID | Milestone | Title | Owner | Effort (pts) | Weight (%) | State | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `task-101` | `ms-01` | Establish canonical governance documents | Edward + AI | 3 | 14 | `done` | Initial repository governance baseline created. |
| `task-102` | `ms-01` | Create modular repository layout for backend, sdk, and ui | Edward + AI | 3 | 14 | `done` | Layout added for PyCharm-friendly project root. |
| `task-103` | `ms-02` | Define runtime domain models and workflow schema contracts | Edward | 5 | 24 | `done` | GitHub issue: #1. Includes Python runtime models and shared schema boundary. |
| `task-104` | `ms-02` | Implement workflow loader and serial engine loop | Edward | 5 | 24 | `done` | Based on `PocPlan.md`. Includes restructuring the example module. |
| `task-105` | `ms-03` | Design UI graph model for drag-and-drop workflows | Edward | 5 | 24 | `planned` | GitHub issue: #7. Must stay aligned with canonical workflow schema. |
| `task-106` | `ms-03` | Define user-visible progress reporting and agile issue/discussion flow | Edward + AI | 3 | 14 | `done` | User-visible progress and GitHub issue/discussion operating rules are documented in the governance files. |
| `task-107` | `ms-02` | Add runnable scripts for backend, tests, and local bootstrap flows | Edward + AI | 3 | 14 | `done` | GitHub issue: #6. The repo must expose simple scripts to run the product and validation flows. |
| `task-108` | `ms-02` | Design Python runtime dependency detection and on-run installation flow | Edward | 5 | 24 | `done` | GitHub issue: #5. The application must detect missing libraries and bootstrap them dynamically when possible. |
| `task-109` | `ms-02` | Enforce 100 percent automated test coverage for core and shared contracts | Edward + AI | 5 | 24 | `done` | GitHub issue: #4. Coverage target is strict and should be automated in the test run path. |
| `task-110` | `ms-01` | Define timestamp-based versioning standard | Edward + AI | 2 | 10 | `done` | GitHub issue: #3. The canonical format is documented and a release metadata workflow emits the timestamp stamp. |
| `task-111` | `ms-02` | Create CI pipelines for testing, validation, and release flows | Edward + AI | 5 | 24 | `done` | GitHub issue: #2. CI test workflow exists and release metadata automation has been added. |

## Effort Summary

- Total effort: 44 pts
- Completed: 39 pts
- In progress: 0 pts
- Remaining: 5 pts

## State Definitions

- `planned`: identified but not ready to start
- `ready`: clarified and available for execution
- `in_progress`: actively being worked on
- `in_review`: implementation complete and under review
- `blocked`: cannot proceed due to an active impediment
- `done`: accepted and completed

## Change Management

Update this document whenever task scope or state changes. Reflect the same changes in the relevant project YAML and in [BITACORA.md](/home/edward/Development/MagnetarPrometheus/BITACORA.md).
