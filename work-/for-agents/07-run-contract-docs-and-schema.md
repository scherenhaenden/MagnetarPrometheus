# Agent 07 Prompt: Run Contracts And Schema Docs

## First Read These Files

Read these before changing anything:

1. `RULES.md`
2. `PLAN.md`
3. `STATUS.md`
4. `ARCHITECTURE.md`
5. `sdk/schemas/README.md`
6. `sdk/schemas/workflow-graph-schema.md`

## Mission

Document the missing contract layer between the current engine and the future visible product surfaces, especially around runs, jobs, and execution inspection.

## Why This Matters

The last conversations made clear that the repo has an engine but lacks a visible application model. One reason is that “run a workflow,” “observe a run,” and “inspect results” are still under-documented as product contracts.

## Your Ownership

You own only:

- `sdk/schemas/README.md`
- new schema docs under `sdk/schemas/`

Do not edit:

- Python SDK models
- backend implementation
- UI files
- root governance docs
- `BITACORA.md`

## Concrete Deliverable

Add documentation that explains concepts such as:

- run submission
- run lifecycle
- run status model
- run result envelope
- how a future UI or API would talk about executions

These docs should bridge today’s CLI proof of concept and tomorrow’s visible product.

## User-Increment Requirement

This is documentation work, but it must still support a near-term user-visible increment by making future API/UI work less ambiguous and more consistent.

## Collision Avoidance

Do not add code here. Stay in schema and contract docs only.

## Completion Standard

You are done when:

- the schema docs explain run-oriented product concepts clearly
- the docs align with the current engine reality
- the docs help later API/UI contributors avoid inventing conflicting models
