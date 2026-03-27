# Agent 04 Prompt: Web UI MVP Shell

## First Read These Files

Read in order:

1. `RULES.md`
2. `PLAN.md`
3. `STATUS.md`
4. `ARCHITECTURE.md`
5. `ui/README.md`
6. `README.md`

This repo currently lacks any visible app surface. Your job is to start changing that without colliding with backend work.

## Mission

Create the smallest possible web UI shell that makes the product feel less invisible.

## Why This Matters

The user explicitly said the current experience is confusing because:

- something runs
- JSON appears
- then it exits
- there is no visible application layer

This task should create a UI shell that can later connect to the backend/API work, even if it starts with static or mocked data.

## Your Ownership

You own only:

- `ui/`
- new files and folders under `ui/`

Do not edit:

- backend code
- sdk files
- root governance docs
- `BITACORA.md`
- scripts

## Concrete Deliverable

Build a first visible UI shell that conveys:

- this is MagnetarPrometheus
- workflows/runs are a first-class concept
- there is or will be a run panel, workflow panel, and status area

An acceptable first increment may include:

- a static or mocked dashboard
- a run console screen
- a workflow selector screen
- a “Run Example Workflow” interaction stub

## User-Increment Requirement

By the end, a user should be able to open something visual and understand the intended product direction immediately, even if the backend integration is partial.

## Constraints

- Keep the write scope entirely inside `ui/`.
- If you need backend integration and it does not exist yet, use mocks and document assumptions in code comments if necessary.
- Favor clarity and product comprehension over completeness.

## Collision Avoidance

Do not reach into API/runtime code. Other agents may be defining the service boundary.

Assume the backend/API contract may still move slightly, so keep integration loose.

## Completion Standard

You are done when:

- `ui/` contains a real visible app shell, not just placeholder text
- the UI communicates what the product is trying to become
- the UI can be shown to a user as a meaningful incremental step
