# Agent 15 Prompt: Frontend Design System And Layout


## Implementation Status (2026-04-07)

- **State:** Completed on this branch.
- **Completion:** **100%** for packet scope.

## First Read These Files

Read in this order:

1. `README.md`
2. `RULES.md`
3. `CONTRIBUTING.md`
4. `PLAN.md`
5. `STATUS.md`
6. `ARCHITECTURE.md`
7. `ui/README.md` if it exists
8. `BITACORA.md`

## Mission

Create the reusable layout primitives and design-token foundation for the
Angular application shell.

## Hard Constraints

- Angular web surface only. No React.
- This is not a branding exercise detached from product reality.
- Keep comments/docstrings very explicit and long.
- Do not implement data services or backend integration here.

## Your Ownership

You own only:

- design tokens
- theme variables
- shared shell primitives
- reusable layout components
- visual structure helpers

Do not edit:

- backend files
- desktop files
- frontend data services
- feature page logic
- `BITACORA.md`

## Concrete Deliverable

Create reusable UI primitives for:

- app frame
- top bar
- side navigation
- content section wrapper
- page header
- status badge treatment
- panel/card/list layout primitives

## Design Direction

- intentional
- product-like
- not generic starter boilerplate
- suitable for a workflow/orchestration tool

## Completion Standard

You are done when:

- the Angular app has a reusable visual/layout base
- future feature slices can be built without redoing shell structure
- the styling system is documented clearly enough that future agents do not
  randomly fork patterns
