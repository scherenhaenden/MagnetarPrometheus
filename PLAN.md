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
| `task-103` | `ms-02` | Define runtime domain models and workflow schema contracts | Edward | 5 | 24 | `ready` | Includes Python runtime models and shared schema boundary. |
| `task-104` | `ms-02` | Implement workflow loader and serial engine loop | Edward | 5 | 24 | `planned` | Based on `PocPlan.md`. |
| `task-105` | `ms-03` | Design UI graph model for drag-and-drop workflows | Edward | 5 | 24 | `planned` | Must stay aligned with canonical workflow schema. |
| `task-106` | `ms-03` | Define user-visible progress reporting and agile issue/discussion flow | Edward + AI | 3 | 14 | `ready` | Add user-perspective status tracking and GitHub issue/discussion operating rules. |

## Effort Summary

- Total effort: 24 pts
- Completed: 6 pts
- In progress: 0 pts
- Remaining: 18 pts

## State Definitions

- `planned`: identified but not ready to start
- `ready`: clarified and available for execution
- `in_progress`: actively being worked on
- `in_review`: implementation complete and under review
- `blocked`: cannot proceed due to an active impediment
- `done`: accepted and completed

## Change Management

Update this document whenever task scope or state changes. Reflect the same changes in the relevant project YAML and in [BITACORA.md](/home/edward/Development/MagnetarPrometheus/BITACORA.md).
