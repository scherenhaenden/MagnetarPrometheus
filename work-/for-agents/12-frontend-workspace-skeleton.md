# Agent 12 Prompt: Frontend Workspace Skeleton

## Implementation Status (2026-04-07)

- **State:** Completed on this branch.
- **Evidence:** Angular workspace under `ui/` compiles, has route foundation, environments, and feature-area directory structure.
- **Completion:** **100%** for packet 12 scope.


## First Read These Files

Read in this order:

1. `README.md`
2. `RULES.md`
3. `CONTRIBUTING.md`
4. `PLAN.md`
5. `STATUS.md`
6. `ARCHITECTURE.md`
7. `TESTING.md`
8. `WIP_GUIDELINES.md`
9. `BRANCHING_MODEL.md`
10. `BITACORA.md`
11. `DAY_PLAN.md` if present

## Mission

Create the Angular workspace and directory skeleton for the first real
application surface of MagnetarPrometheus.

## Hard Constraints

- Angular only. No React.
- TypeScript-first.
- Add extremely explicit top-of-file comments and intent documentation.
- Do not build feature content yet.
- Do not implement desktop shell work here.
- Do not invent backend logic in the frontend.

## Your Ownership

You own only the Angular workspace and structural files under `ui/`.

Do not edit:

- backend runtime files
- SDK files
- desktop-shell files
- issue/planning docs outside what is directly needed for UI run instructions
- `BITACORA.md`

## Concrete Deliverable

Create a clean Angular workspace under `ui/` with:

- app entrypoint
- routing foundation
- core app structure
- shared component/layout directory
- feature-area directories for future work
- environment files
- package scripts needed to run the shell

## Why This Matters

The repo has backend and CLI reality, but not a real app shell. The workspace
must make the UI feel like a first-class subsystem rather than a placeholder.

## Completion Standard

You are done when:

- the Angular workspace exists and compiles
- the structure is obvious for future contributors
- comments/docstrings are intentionally long and explicit
- the result prepares the repo for real product slices without pretending they
  are already implemented
