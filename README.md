# MagnetarPrometheus

MagnetarPrometheus is a workflow orchestration platform that follows the Magnetar Canonical Project Model for documentation, planning, and governance. It is not the canonical model repository itself. It is a product repository that uses the canon as its operating standard.

The platform goal is twofold:

- provide a modular runtime for declarative, stateful, branching workflows
- evolve toward a visual workflow builder where complete flows can be composed through click, drag, and drop interactions

The first implementation target is Python, but the architecture is intentionally split so that the backend runtime, shared SDK/schema contracts, and future visual editor can evolve independently.

## Purpose

MagnetarPrometheus exists to orchestrate business and technical workflows without hardwiring process logic into application code. Workflows should be modeled as data, executed by a controlled engine, observed through structured runtime state, and eventually authored visually through a workflow editor.

This repository follows the Magnetar standard for:

- documentation discipline
- planning and state tracking
- branching and work-in-progress governance
- blocker handling and escalation

It should be run in an agile way. Progress tracking must not stop at technical implementation details. Daily visibility should include what a user can already do, what changed in the product experience, and what remains blocked from a user-facing perspective.

The working style for this repository is explicitly user-incremental. Each meaningful round of work should leave behind something new that a user or operator can actually try, observe, or validate, even if the increment is still rough or limited.

## Product Boundaries

This repository contains a product that uses the canonical model. The canonical model itself is a separate concept used to administer projects.

The intended repository split is:

```text
MagnetarPrometheus/
  backend/                # Python orchestration engine and runtime
  sdk/                    # Shared contracts, schemas, and client helpers
  ui/                     # Future visual workflow builder
  docs/                   # Supporting documentation and examples
  projects/               # Canonical machine-readable project records
  PLAN.md
  BITACORA.md
  REQUIREMENTS.md
  ARCHITECTURE.md
  RULES.md
  STATUS.md
  TESTING.md
  BLOCKERS.md
  BRANCHING_MODEL.md
  WIP_GUIDELINES.md
  CONTRIBUTING.md
  PocPlan.md
  README.md
```

## How to Use This Repository

1. Read [PocPlan.md](/home/edward/Development/MagnetarPrometheus/PocPlan.md) for the architectural intent of the PoC runtime.
2. Read [ARCHITECTURE.md](/home/edward/Development/MagnetarPrometheus/ARCHITECTURE.md), [REQUIREMENTS.md](/home/edward/Development/MagnetarPrometheus/REQUIREMENTS.md), and [PLAN.md](/home/edward/Development/MagnetarPrometheus/PLAN.md) before implementation work.
3. Use [projects/_template.project.yml](/home/edward/Development/MagnetarPrometheus/projects/_template.project.yml) as the canonical machine-readable project schema reference.
4. Keep work aligned with [RULES.md](/home/edward/Development/MagnetarPrometheus/RULES.md), [BRANCHING_MODEL.md](/home/edward/Development/MagnetarPrometheus/BRANCHING_MODEL.md), and [WIP_GUIDELINES.md](/home/edward/Development/MagnetarPrometheus/WIP_GUIDELINES.md).
5. Record every meaningful state change, decision, and exception in [BITACORA.md](/home/edward/Development/MagnetarPrometheus/BITACORA.md).
6. Use the example repository structure under `backend/`, `sdk/`, and `ui/` to keep runtime, contracts, and visual tooling decoupled.
7. Use GitHub issues for actionable work items and GitHub discussions for broader architectural, product, and governance conversations.

## Run The Application

The current runnable product slice is the backend workflow runner. From the repository root, use:

```bash
bash run_app.sh
```

That single command will:

- bootstrap the local Python environment if needed
- install the runtime dependencies required by the PoC
- execute the example workflow
- print the resulting workflow state as JSON in the terminal

To run a specific workflow file instead of the default example:

```bash
bash run_app.sh --workflow backend/src/magnetar_prometheus/modules/email_module/email_triage.yaml
```

A first browser-based Angular shell now exists under `ui/` and runs in mock transport mode.

From repository root:

```bash
cd ui
npm ci
npm run start
```

The CLI workflow runner remains the primary fully-integrated runtime entrypoint while API-backed UI mode is still in progress.

## Project Contents

| File | Purpose |
| --- | --- |
| `PLAN.md` | Project tasks, milestones, and planning baseline. |
| `BITACORA.md` | Chronological logbook of decisions, discoveries, and state changes. |
| `REQUIREMENTS.md` | Functional and non-functional requirements. |
| `ARCHITECTURE.md` | System structure, module boundaries, and key technical decisions. |
| `RULES.md` | Naming rules, workflow rules, and required governance standards. |
| `STATUS.md` | Current health summary, milestone status, and risks. |
| `TESTING.md` | Testing strategy, coverage goals, and reporting rules. |
| `BLOCKERS.md` | Tracked blockers and escalation paths. |
| `BRANCHING_MODEL.md` | Git branching and merge policy. |
| `WIP_GUIDELINES.md` | Work-in-progress limits and exception handling. |
| `CONTRIBUTING.md` | Contributor setup and pull request expectations. |
| `projects/_template.project.yml` | Canonical machine-readable project schema template. |

## Progress Model Overview

Work is tracked through milestones and tasks. Each task must use one of the allowed state transitions:

`planned` -> `ready` -> `in_progress` -> `in_review` -> `done`

(Note: "done" must not imply a finished product experience if only an internal slice is complete).

When necessary, tasks may move into `blocked`, but that state must be reflected in [BLOCKERS.md](/home/edward/Development/MagnetarPrometheus/BLOCKERS.md) and summarized in [STATUS.md](/home/edward/Development/MagnetarPrometheus/STATUS.md).

Every state change must be logged in [BITACORA.md](/home/edward/Development/MagnetarPrometheus/BITACORA.md).

In addition, daily status should answer user-facing questions, not just implementation questions:

- what is now possible for a user or operator
- what is visible in the product or workflow editor
- what remains missing before a usable increment exists

The preferred delivery rhythm is:

- every round trip should aim to make one more thing runnable, visible, or testable
- internal refactors are allowed, but they should be tied to a near-term user-visible increment whenever possible
- parallel work must be divided by disjoint write ownership
- documentation must state clearly whether a change is user-visible or internal-only; when a slice is not yet user-visible, the docs must say so directly instead of overstating completion

## YAML Project Schema

The file [projects/_template.project.yml](/home/edward/Development/MagnetarPrometheus/projects/_template.project.yml) defines the canonical machine-readable project schema. It captures:

- metadata
- stakeholders
- milestones
- tasks
- risks
- reporting hooks

This repository uses that structure to align human-readable documents with machine-readable planning data.

## Guidance For AI Collaborators

AI collaborators working in this repository should:

- parse the project YAML before acting on planning-sensitive work
- use [PLAN.md](/home/edward/Development/MagnetarPrometheus/PLAN.md) and [STATUS.md](/home/edward/Development/MagnetarPrometheus/STATUS.md) to determine current focus
- respect [RULES.md](/home/edward/Development/MagnetarPrometheus/RULES.md), [WIP_GUIDELINES.md](/home/edward/Development/MagnetarPrometheus/WIP_GUIDELINES.md), and [BRANCHING_MODEL.md](/home/edward/Development/MagnetarPrometheus/BRANCHING_MODEL.md)
- update [BITACORA.md](/home/edward/Development/MagnetarPrometheus/BITACORA.md) after completing any substantial work
- keep the distinction clear between this product repository and the separate canonical model concept
- prefer keeping actionable work represented in GitHub issues and broader open questions in GitHub discussions

## Architecture Flow

```text
Magnetar Canonical Model
        |
        v
Governance + Planning Rules
        |
        v
Project Docs + YAML Schema
        |
        v
Backend Runtime <-> SDK/Schema Contracts <-> Visual Workflow UI
        |
        v
Executable Workflows and Managed Project Delivery
```

## Applying This Structure

To use this structure correctly:

1. Keep the repository root as the IDE project root.
2. Implement the Python runtime inside `backend/`.
3. Place language-neutral contracts and shared schemas inside `sdk/`.
4. Build the future workflow designer inside `ui/`.
5. Instantiate a real project record from [projects/_template.project.yml](/home/edward/Development/MagnetarPrometheus/projects/_template.project.yml).
6. Establish initial milestones and tasks in [PLAN.md](/home/edward/Development/MagnetarPrometheus/PLAN.md), [STATUS.md](/home/edward/Development/MagnetarPrometheus/STATUS.md), and [BITACORA.md](/home/edward/Development/MagnetarPrometheus/BITACORA.md).

## IDE Recommendation

Open `/home/edward/Development/MagnetarPrometheus` directly in PyCharm. Do not create a second nested top-level project directory. Keep the repo root as the project root and let the Python code live under `backend/src/`.

This gives you:

- clean packaging for Python
- room for a separate UI app later
- a stable place for shared schemas and SDK code
- a structure that scales to multiple IDEs without repo surgery

## Canon Compliance Checklist

- required governance files exist at the repository root
- the project YAML follows the canonical schema template
- [BITACORA.md](/home/edward/Development/MagnetarPrometheus/BITACORA.md) is chronological and append-only by correction
- active branches follow [BRANCHING_MODEL.md](/home/edward/Development/MagnetarPrometheus/BRANCHING_MODEL.md)
- testing and blocker handling match [TESTING.md](/home/edward/Development/MagnetarPrometheus/TESTING.md) and [BLOCKERS.md](/home/edward/Development/MagnetarPrometheus/BLOCKERS.md)
