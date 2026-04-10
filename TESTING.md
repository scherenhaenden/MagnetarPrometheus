# Testing Strategy for MagnetarPrometheus

## Current Testing Reality

The current automated test suite validates the backend proof-of-concept slice very aggressively, but it does not validate a finished end-user product because that product surface does not exist yet.

For a few touched operational files, the backend pytest suite now also enforces a narrow
documentation contract. That check exists because docstring coverage alone was not enough to
stop intent comments from being trimmed below the repository's preferred "explain the why,
how, what, and keep-it-this-way constraint" threshold.

What is covered well today:

- workflow model validation
- workflow loading
- step execution
- next-step resolution
- conditional evaluation
- executor routing
- bootstrap and dependency-policy behavior
- CLI/module wiring for the current backend slice

What is not covered yet because it does not exist yet:

- web UI behavior
- desktop UI behavior
- API endpoints
- persistent job/run storage
- end-user session flows
- queueing/scheduling behavior

## Validation Tiers

As the product expands from a backend engine into a visible service and application, validation is organized into explicit tiers. These tiers can be targeted using `bash scripts/run_tests.sh <tier>`.

Today, `bash scripts/run_tests.sh` runs backend and UI tiers. The API tier remains placeholder-only and returns non-zero when selected explicitly.

### 1. Backend (`tier: backend`)
- Currently active and enforced at 100% code coverage.
- Unit tests for domain models, validation, next-step resolution, and executor routing
- Integration tests for full workflow execution using mock modules
- Contract tests for shared SDK/schema compatibility between backend and UI-facing payloads

### 2. API (`tier: api`)
- *Future placeholder.*
- Will contain integration and contract tests validating the HTTP service boundary, job submission, and result retrieval.

### 3. UI (`tier: ui`)
- **Implemented.**
- Angular unit/smoke tests execute through `npm run test:ci`.
- The Angular UI tier now enforces `100%` coverage for statements, branches, functions, and lines through `ui/karma.conf.cjs`.
- Root-level integration executes `scripts/check_ui_code_contracts.py`, `npm run build`, and `npm run test:ci` via `bash scripts/run_tests.sh ui`.

## Code Coverage

- Backend automated test target: 100% coverage on core orchestration code
- Shared schema and SDK target: 100% coverage on validation and transformation logic
- Angular UI automated test target: 100% coverage on statements, branches, functions, and lines
- Bootstrap and dependency-detection flows must also be covered, including success, install-needed, install-failed, and policy-disabled paths

## Acceptance Criteria

- A sample workflow can load, execute, branch, and produce a deterministic context output
- Invalid workflow definitions fail validation clearly
- Shared schema artifacts can round-trip between editor-facing and runtime-facing representations
- Runtime startup detects missing dependencies before execution proceeds
- Automatic dependency installation behavior is validated under controlled test scenarios

For the current proof of concept, acceptance should be read as “the backend slice behaves correctly.” It should not be read as “the full application experience is complete.”

## Coverage Enforcement

- Coverage thresholds should be enforced in the standard test run path
- Pull requests should not be considered complete if they reduce the enforced threshold

## Pipeline Expectations

- CI must execute the standard test and validation path on every relevant change
- coverage enforcement must run in pipeline, not only locally
- release-oriented pipeline stages should preserve the canonical version stamp format `yyyy.MM.dd HH:mm:ss.SSS`

## Validating The Current User Increment

Because the current visible product increment is a CLI application rather than a web UI, validation focuses on engine behavior and schema contracts.

To validate the product locally from the repository root:

```bash
bash run_app.sh
bash run_app.sh --api --daemon start --port 8010
bash run_app.sh --api --daemon status --port 8010
bash run_app.sh --api --daemon stop --port 8010
bash scripts/run_tests.sh
```

These commands validate both the visible surface (the CLI) and the internal correctness (the engine tests):

- `run_app.sh` proves the backend can bootstrap and execute the example workflow
- `run_app.sh --api --daemon ...` proves the repo-root launcher can manage the minimal API lifecycle with explicit local bind controls
- `scripts/run_tests.sh` proves the implemented backend, SDK, and UI scopes still satisfy the enforced coverage contracts

## Bug Reporting Process

1. Record the defect in the team tracking system.
2. If the bug blocks progress, add it to [BLOCKERS.md](/home/edward/Development/MagnetarPrometheus/BLOCKERS.md).
3. Reflect impact in [STATUS.md](/home/edward/Development/MagnetarPrometheus/STATUS.md) when material.
4. Log key diagnosis and resolution steps in [BITACORA.md](/home/edward/Development/MagnetarPrometheus/BITACORA.md).
