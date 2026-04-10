# Agent 14 Prompt: Frontend Data Contract Boundary


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
7. `TESTING.md`
8. `sdk/schemas/README.md`
9. relevant run/job schema docs in `sdk/schemas/`
10. `BITACORA.md`

## Mission

Create the frontend-side type and service boundary that will sit between the
Angular UI and the future HTTP API.

## Hard Constraints

- Angular ecosystem only. No React.
- Do not place transport details directly in page components.
- Keep comments/docstrings extremely explicit.
- Use mock adapters and service interfaces instead of fake business logic in UI.

## Your Ownership

You own only:

- frontend-facing interfaces/models
- API facade or service boundary
- mock transport adapters
- mapping helpers directly related to frontend data ingress

Do not edit:

- app shell layout
- design system files
- desktop host files
- backend implementation files
- `BITACORA.md`

## Concrete Deliverable

Create frontend-facing contracts for:

- service health/status
- run listing/history
- run detail
- job submission request/result
- workflow summary metadata

And provide:

- a stable service boundary
- a mock implementation
- a clear seam where the future HTTP implementation will attach

## Completion Standard

You are done when:

- routed pages can depend on frontend services instead of raw transport shapes
- a mock mode can support UI work before the HTTP API is complete
- the contract boundary is heavily documented and difficult to misread
