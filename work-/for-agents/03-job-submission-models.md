# Agent 03 Prompt: Job Submission Models

## First Read These Files

Read these first:

1. `RULES.md`
2. `PLAN.md`
3. `STATUS.md`
4. `ARCHITECTURE.md`
5. `sdk/schemas/workflow-graph-schema.md`
6. `sdk/python/src/magnetar_prometheus_sdk/models.py`

The work must respect the current boundary between backend runtime internals and shared contracts.

## Mission

Define the minimal shared contract for “submit a run / inspect a run” so the project can evolve from pure CLI execution toward an actual application with jobs or runs.

## Why This Matters

The recent conversations exposed a gap:

- there is an engine
- there are workflows
- there is no clear contract for submitting a job/run into a longer-lived application surface

This task should create that contract boundary without prematurely overbuilding it.

## Your Ownership

You own only:

- `sdk/python/src/magnetar_prometheus_sdk/models.py`
- `sdk/python/tests/test_models.py`
- new files under `sdk/schemas/` that define run/job contract details

Do not edit:

- backend runtime implementation files
- `BITACORA.md`
- `PLAN.md`
- `STATUS.md`
- `README.md`
- `ui/`

## Concrete Deliverable

Add shared models or schema definitions for concepts such as:

- run submission request
- run response
- run summary
- run status
- run listing item

Keep these contracts compatible with the current backend proof of concept and plausible for future UI/API use.

## User-Increment Requirement

Even though this is contract work, it must still serve a near-term user-visible increment by making it possible for other surfaces to expose:

- “run this workflow”
- “show me this run”
- “list recent runs”

The contract should reduce ambiguity for the next product slice.

## Suggested Steps

1. Review existing workflow and step models.
2. Introduce only the minimum additional models required.
3. Add validation and tests.
4. If helpful, add one schema markdown explaining the intent and field meanings.

## Collision Avoidance

Do not edit API files, UI files, engine files, or governance docs. Your scope is the shared contract layer only.

Avoid inventing transport-specific details unless they are unavoidable.

## Completion Standard

You are done when:

- the repo has a minimal shared run/job contract
- tests cover the new models
- the design is clearly consumable by both backend and future UI/API work
