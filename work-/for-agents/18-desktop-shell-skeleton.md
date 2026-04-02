# Agent 18 Prompt: Desktop Shell Skeleton

## First Read These Files

Read in this order:

1. `README.md`
2. `RULES.md`
3. `CONTRIBUTING.md`
4. `PLAN.md`
5. `STATUS.md`
6. `ARCHITECTURE.md`
7. `BITACORA.md`

## Mission

Create the desktop host skeleton that can wrap the Angular application without
forking the UI into a second frontend stack.

## Hard Constraints

- Do not use React.
- The web app remains Angular.
- Keep comments and docstrings extremely explicit and long.
- Prefer Electron unless you can justify another desktop wrapper very clearly.
- Do not implement desktop-only business features yet.

## Your Ownership

You own only:

- desktop shell directory and config
- main/preload/process skeleton
- secure bridge placeholder
- dev/prod wiring for loading the Angular app

Do not edit:

- backend runtime files
- Angular feature implementation files
- frontend data models unless absolutely needed for a bridge contract
- `BITACORA.md`

## Concrete Deliverable

Create a desktop shell skeleton with:

- app entrypoint
- window creation flow
- preload/bridge placeholder
- secure IPC placeholder structure
- clear explanation of what remains desktop-only versus shared with the Angular app

## Completion Standard

You are done when:

- the repo has a credible desktop host starting point
- the Angular UI remains the shared product surface
- the comments make it hard for future agents to leak desktop concerns into ordinary UI components
