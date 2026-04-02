# Agent 13 Prompt: Frontend Web Shell

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
11. `ui/README.md` if it exists

## Mission

Build the first real browser-visible Angular shell for MagnetarPrometheus.

## Hard Constraints

- Angular only. No React.
- Keep comments and docstrings very long and explicit.
- This is a shell, not the full product.
- Do not implement desktop host logic here.
- Do not hardcode fake backend data directly in page components.

## Your Ownership

You own only:

- Angular app shell files
- top-level routed pages
- shell navigation and layout wiring

Do not edit:

- backend files
- desktop shell files
- frontend transport/data contract files unless absolutely required
- `BITACORA.md`

## Concrete Deliverable

Create a routed web shell with:

- a top app frame
- navigation
- overview page
- runs/history page placeholder
- workflow-details page placeholder
- job-submission page placeholder
- settings or environment page placeholder
- service status indicator area

## User-Centered Requirement

A user should be able to open the browser and immediately understand:

- this is the start of a workflow platform
- where runs will appear
- where job submission will happen
- where workflow details will be browsed

## Completion Standard

You are done when:

- the shell is visually coherent
- navigation works
- placeholder pages explain what future real data belongs there
- code comments make layout/data/route boundaries very hard to misunderstand
