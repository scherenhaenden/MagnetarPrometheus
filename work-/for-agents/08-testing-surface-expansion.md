# Agent 08 Prompt: Testing Surface Expansion

## First Read These Files

Read in this order:

1. `RULES.md`
2. `TESTING.md`
3. `STATUS.md`
4. `ARCHITECTURE.md`
5. `scripts/run_tests.sh`
6. `backend/pyproject.toml`

## Mission

Improve the testing/documented validation path so future visible product slices can be added without the testing story staying locked to “engine internals only.”

## Why This Matters

The project currently has strong coverage on the backend proof-of-concept slice, but future API/UI/service work will need a clearer validation path.

## Your Ownership

You own only:

- `TESTING.md`
- `scripts/run_tests.sh`
- `backend/pyproject.toml`
- new test helpers or test docs that are directly related to validation flow

Do not edit:

- root planning docs
- UI files
- SDK models
- runtime implementation files
- `BITACORA.md`

## Concrete Deliverable

Make the testing surface easier to understand and extend for the next slices. Good outcomes include:

- clarifying test tiers
- making future API/UI test slots explicit
- improving the top-level validation script structure
- documenting how to validate the current user-visible increment versus internal correctness

## User-Increment Requirement

The result should help contributors and users validate newly added visible surfaces in later rounds without confusion.

## Collision Avoidance

Do not rewrite product architecture here. This is about validation structure and testing flow only.

## Completion Standard

You are done when:

- the validation path is clearer
- future visible slices have an obvious place in the testing story
- the work stays confined to testing/validation ownership
