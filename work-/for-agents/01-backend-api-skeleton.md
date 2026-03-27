# Agent 01 Prompt: Backend API Skeleton

## First Read These Files

Before writing code, read these files in this order:

1. `RULES.md`
2. `PLAN.md`
3. `STATUS.md`
4. `ARCHITECTURE.md`
5. `README.md`
6. `WIP_GUIDELINES.md`

Do not skip the rules pass. This repo has explicit documentation, merge, and user-increment expectations.

## Mission

Create the first minimal backend API surface around the existing workflow engine so the project moves one step closer to a visible application instead of remaining CLI-only.

The goal is not a full production service. The goal is a thin, testable, local API skeleton that makes the engine callable through a stable boundary.

## Why This Matters

From the latest conversations:

- the engine exists
- the CLI works
- there is still no persistent or visible application surface
- the project must now advance in user-incremental slices

This task should create one new thing the user can test directly: a local API process or API-like callable boundary.

## Your Ownership

You own only these paths:

- `backend/src/magnetar_prometheus/api/`
- `backend/tests/test_api*.py`
- if needed, a new API-focused module imported from `backend/src/magnetar_prometheus/cli.py`, but do not edit the CLI unless strictly necessary

Do not edit:

- `BITACORA.md`
- `PLAN.md`
- `STATUS.md`
- `README.md`
- `sdk/`
- `ui/`
- existing engine internals unless absolutely blocked

## Concrete Deliverable

Implement a minimal local API skeleton that can:

- expose a health endpoint or equivalent basic response
- expose a “run workflow” entrypoint for the existing example workflow
- return JSON responses based on the existing engine output

Keep the scope intentionally small. A good outcome is a tiny HTTP or service boundary that proves the runtime can be reached without going through the current one-shot CLI path only.

## Constraints

- Reuse the existing engine, loader, router, registry, context manager, and example step registration.
- Do not rewrite core runtime logic unless required for API extraction.
- If you need framework choice, prefer the smallest practical option already consistent with the repo direction. If adding a dependency would create unnecessary churn, keep the API layer lightweight and explicit.
- Keep code understandable and easy to test.

## User-Increment Requirement

By the end of your slice, a contributor should be able to test something new beyond `bash run_app.sh`.

Examples of acceptable user-testable outcomes:

- start a local process and hit `/health`
- call `/run-example` and receive JSON
- invoke a minimal local API command that clearly behaves like a service boundary

## Suggested Steps

1. Read the current backend CLI and engine wiring.
2. Extract or reuse the runtime assembly code cleanly.
3. Add a small API module with one or two endpoints only.
4. Add focused tests for the new surface.
5. Keep the write scope narrow.

## Collision Avoidance

Do not touch docs, schemas, UI files, or job persistence designs. Other agents may own those.

If you discover you need persistence, create a TODO in code and stop at an in-memory path rather than editing another agent’s ownership area.

## Completion Standard

You are done when:

- the repo has a minimal API surface
- tests for that surface exist
- the new surface exercises the current workflow engine
- the change clearly advances the project toward a visible app layer
