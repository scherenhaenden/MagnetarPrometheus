# Agent 02 Prompt: Run Store And History

## First Read These Files

Read before changing anything:

1. `RULES.md`
2. `PLAN.md`
3. `STATUS.md`
4. `ARCHITECTURE.md`
5. `TESTING.md`

The repo rules require user-incremental delivery and disjoint work ownership. Follow them literally.

## Mission

Design and implement the smallest useful in-repo run history layer so execution results do not only flash by in terminal JSON and disappear.

## Why This Matters

Current product limitation:

- workflow runs are one-shot
- output is printed
- there is no run history
- there is no inspectable trail except manual console output

This task should move the product toward an inspectable application surface.

## Your Ownership

You own only:

- `backend/src/magnetar_prometheus/run_store.py`
- `backend/src/magnetar_prometheus/history/`
- `backend/tests/test_run_store.py`
- `backend/tests/test_history*.py`

You may create new files in those areas.

Do not edit:

- `BITACORA.md`
- `PLAN.md`
- `STATUS.md`
- `README.md`
- `ui/`
- `sdk/`
- `backend/src/magnetar_prometheus/core/engine.py` unless absolutely unavoidable

## Concrete Deliverable

Add a simple local run-history mechanism that can store:

- run id
- workflow id
- start/end timestamps
- status
- output snapshot or summary
- error list if present

Keep it lightweight. File-based JSON or in-memory plus serialization is acceptable. The point is not durability perfection; the point is that runs become inspectable after execution.

## User-Increment Requirement

Create a capability that makes a new user-visible behavior possible, for example:

- after running a workflow, there is a recorded run artifact
- a local helper can list or load previous runs
- a future API/UI can consume this without inventing storage later

## Suggested Steps

1. Inspect the shape of `RunContext`.
2. Create a store abstraction with a tiny, explicit interface.
3. Provide a default local implementation.
4. Add tests that verify save/load/list semantics.
5. Keep engine changes minimal or avoid them entirely if you can integrate through a higher layer.

## Collision Avoidance

Do not build the API, do not build the UI, and do not change schema docs here. Those belong to other slices.

If another surface needs this store later, keep your interface small and stable rather than coupling it to a specific transport.

## Completion Standard

You are done when:

- run records can be stored and retrieved
- tests exist
- the abstraction is reusable by a later API or UI
- the work clearly reduces the “CLI output disappears immediately” limitation
