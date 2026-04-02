# Day Plan

## Date

`2026-04-02`

## Purpose

Today should move MagnetarPrometheus in a more user-centered direction.

The current backend/runtime slice works, but the product still feels invisible to a user because the main experience is still "run a command, see output, exit."

This file is the execution plan for today only. It is intentionally narrower and more concrete than `PLAN.md`.

## Today's User Goal

By the end of today's work, a user should be able to see more of the product and understand what happened during a run without needing to inspect raw code or guess from terminal output.

## Priority Order

1. Put a visible product surface in front of the current runtime.
2. Make the example run flow obvious and legible.
3. Leave behind visible evidence of execution that a user can inspect.
4. Update the docs so they describe what the user can actually see today.

## Concrete Execution Scope

The preferred implementation path for today is:

1. improve the CLI summary so the batch path is easier to scan
2. serve a first local UI shell from the existing API/server path
3. let the UI trigger the example workflow through the API
4. show the latest run result in the UI
5. refresh the docs around the new visible slice

## Planned Work

### 1. First visible UI shell

Create or extend the first local UI surface under `ui/` so a user can open something visual and immediately understand:

- what MagnetarPrometheus is
- that workflows and runs are the main concepts
- where a run action will happen
- where status and results will appear

Preferred delivery shape:

- keep the first UI increment small
- favor a simple local shell over framework-heavy setup
- if possible, make it available directly from the existing local API/server entrypoint

### 2. Example run action through the local service boundary

Use the existing local API path as the bridge from UI to engine so the user can trigger the example workflow without relying only on the terminal path.

Minimum acceptable outcome:

- one obvious "run example workflow" action
- clear success or failure feedback
- visible result summary after completion

### 3. Recent run visibility

Add a small "latest run" or "recent activity" surface so execution leaves something behind that the user can see after the action completes.

Minimum acceptable outcome:

- latest workflow id
- latest status
- latest completion state or timestamp
- short result summary or key output fields

### 4. CLI legibility improvement

Keep the CLI path useful while the UI is being introduced.

Minimum acceptable outcome:

- clearer summary output
- more obvious success or failure state
- less need to parse raw JSON unless the user explicitly wants it

### 5. Documentation refresh for the current visible slice

Update the repo docs after the visible increment lands so they answer:

- what a user can open
- what a user can run
- what a user can inspect
- what is still missing

## Verification For Today

Before calling the day successful, validate the visible paths directly:

1. `bash run_app.sh`
2. `bash run_app.sh --api`
3. open the local UI surface and trigger the example run
4. confirm the result is visible without reading terminal JSON

## Working Rule For Today

If a change is not visible, runnable, or inspectable by a user or operator, it should support one of the items above directly and stay small.

## Done For Today Means

Today counts as successful if:

- a user-facing surface is more visible than it was this morning
- the run flow is easier to understand than raw JSON alone
- the product leaves at least one visible artifact of execution
- the docs describe the new visible reality honestly

## Notes

- `PLAN.md` should stay at milestone and backlog level.
- Day-specific execution planning belongs in this file, not in `PLAN.md`.
- If a roadmap change is needed later, reflect it in `PLAN.md` after the visible increment is real, not only proposed.
