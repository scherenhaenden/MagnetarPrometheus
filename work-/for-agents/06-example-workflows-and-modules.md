# Agent 06 Prompt: Example Workflows And Modules

## First Read These Files

Read before making changes:

1. `RULES.md`
2. `README.md`
3. `STATUS.md`
4. `ARCHITECTURE.md`
5. `backend/src/magnetar_prometheus/modules/email_module/email_triage.yaml`
6. `backend/src/magnetar_prometheus/modules/email_module/steps.py`

## Mission

Expand the set of example workflows/modules so the project demonstrates more than a single hardcoded happy path.

## Why This Matters

A single example workflow proves the engine works, but it does not yet show the range of the product.

This task should make the current product slice more understandable and more testable by adding additional runnable examples.

## Your Ownership

You own only:

- `backend/src/magnetar_prometheus/modules/`
- `backend/tests/test_example.py`
- new tests for additional example modules

Do not edit:

- engine core
- sdk files
- root docs
- UI files
- `BITACORA.md`

## Concrete Deliverable

Add one or two additional example workflows or modules that exercise different runtime behaviors, such as:

- a manual-review branch
- an error/failure branch
- a simple linear workflow

Keep them small and deterministic.

## User-Increment Requirement

By the end of this slice, a user should be able to run more than one meaningful example and understand that the engine is not tied to only one scenario.

## Collision Avoidance

Do not redesign the runtime or the schemas. This slice is about examples and demonstration value.

## Completion Standard

You are done when:

- new example module or workflow files exist
- tests cover them
- the examples make the product more demonstrable to a user
