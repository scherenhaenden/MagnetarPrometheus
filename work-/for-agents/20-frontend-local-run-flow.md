# Agent 20 Prompt: Frontend Local Run Flow

## First Read These Files

Read in this order:

1. `README.md`
2. `RULES.md`
3. `CONTRIBUTING.md`
4. `TESTING.md`
5. `PLAN.md`
6. `STATUS.md`
7. `ARCHITECTURE.md`
8. existing `ui/README.md` if present
9. `BITACORA.md`

## Mission

Make the local developer run flow for the frontend/application surface obvious.

## Hard Constraints

- Angular web surface only. No React.
- Keep comments/docstrings and written guidance explicit and long where needed.
- Focus on run path, docs, and developer usability.
- Do not redesign product features here.

## Your Ownership

You own only:

- frontend run instructions
- related npm scripts or local helper scripts
- README updates directly related to the frontend run path
- dev-flow notes needed so contributors know how to start the UI

Do not edit:

- backend implementation files
- Angular feature logic unrelated to run/start flow
- desktop shell internals beyond launch instructions
- `BITACORA.md`

## Concrete Deliverable

Create a local run flow so a contributor can quickly understand:

- how to install frontend dependencies
- how to start the Angular app
- how mock mode works if the backend service is not ready
- how the future API-backed mode will fit in
- how to validate the frontend locally

## Completion Standard

You are done when:

- the repo has a clear local-start story for the new app surface
- a contributor does not have to reverse-engineer how to launch the frontend
- the docs make the boundary between current mock mode and future real API mode explicit
