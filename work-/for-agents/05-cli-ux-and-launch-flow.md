# Agent 05 Prompt: CLI UX And Launch Flow

## First Read These Files

Read before starting:

1. `RULES.md`
2. `README.md`
3. `STATUS.md`
4. `ARCHITECTURE.md`
5. `run_app.sh`
6. `scripts/run_backend.sh`
7. `backend/src/magnetar_prometheus/cli.py`

## Mission

Improve the local launch and CLI experience so the current proof-of-concept is easier to understand when a user runs it.

## Why This Matters

The current backend works, but the experience is still confusing:

- the user runs a command
- bootstrap logs appear
- JSON appears
- the user has to guess what happened

This task should make the CLI experience more legible without changing the whole architecture.

## Your Ownership

You own only:

- `run_app.sh`
- `scripts/run_backend.sh`
- `backend/src/magnetar_prometheus/cli.py`
- `backend/tests/test_cli.py`

Do not edit:

- docs
- sdk
- ui
- engine internals
- `BITACORA.md`

## Concrete Deliverable

Improve the launch flow and CLI output so a user can understand:

- what command was run
- which workflow is being executed
- whether the run succeeded
- where to look next

Examples of acceptable improvements:

- cleaner banners and progress messages
- explicit workflow path reporting
- concise success summary before dumping JSON
- optional `--pretty` or `--summary` modes if useful

## User-Increment Requirement

After this slice, a user who runs the CLI should understand the product better without reading source code first.

## Collision Avoidance

Do not add API endpoints, persistence layers, or UI files. Stay entirely in the launcher/CLI path.

## Completion Standard

You are done when:

- the CLI experience is materially clearer
- tests still cover the behavior
- a first-time user can run the backend and understand what the output represents
