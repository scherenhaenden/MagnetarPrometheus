# Agent 17 Prompt: Frontend Job Submission Slice

## First Read These Files

Read in this order:

1. `README.md`
2. `RULES.md`
3. `CONTRIBUTING.md`
4. `PLAN.md`
5. `STATUS.md`
6. `ARCHITECTURE.md`
7. relevant run/job schema docs in `sdk/schemas/`
8. `BITACORA.md`

## Mission

Build the isolated frontend slice for job submission.

## Hard Constraints

- Angular only. No React.
- Keep comments/docstrings extremely explicit.
- Respect the frontend data-service boundary if it already exists.
- Do not implement run-history browsing here.
- Do not touch desktop shell work.

## Your Ownership

You own only:

- job submission page/feature
- related form state handling
- validation display
- submission-result placeholder handling

Do not edit:

- backend runtime files
- run-history feature files
- desktop shell
- unrelated app-shell files
- `BITACORA.md`

## Concrete Deliverable

Create a frontend feature slice where a user can:

- open a job submission page
- understand what a submission represents
- fill or inspect the submission inputs
- trigger a mock submission through the service boundary
- see placeholder success/error states

## User-Centered Requirement

Even with mock transport, the UI should make the future action obvious:
submit a workflow/job to the service layer rather than just running a CLI.

## Completion Standard

You are done when:

- the feature feels like a real submission surface
- form boundaries and validation points are clear
- future real API integration has obvious attachment points
