# Testing Strategy for MagnetarPrometheus

## Types Of Tests

- Unit tests for domain models, validation, next-step resolution, and executor routing
- Integration tests for full workflow execution using mock modules
- Contract tests for shared SDK/schema compatibility between backend and UI-facing payloads
- Future end-to-end tests for visual workflow creation and serialization

## Code Coverage

- Backend automated test target: 100% coverage on core orchestration code
- Shared schema and SDK target: 100% coverage on validation and transformation logic
- Bootstrap and dependency-detection flows must also be covered, including success, install-needed, install-failed, and policy-disabled paths

## Acceptance Criteria

- A sample workflow can load, execute, branch, and produce a deterministic context output
- Invalid workflow definitions fail validation clearly
- Shared schema artifacts can round-trip between editor-facing and runtime-facing representations
- Runtime startup detects missing dependencies before execution proceeds
- Automatic dependency installation behavior is validated under controlled test scenarios

## Coverage Enforcement

- Coverage thresholds should be enforced in the standard test run path
- Pull requests should not be considered complete if they reduce the enforced threshold

## Pipeline Expectations

- CI must execute the standard test and validation path on every relevant change
- coverage enforcement must run in pipeline, not only locally
- release-oriented pipeline stages should preserve the canonical version stamp format `yyyy.MM.dd HH:mm:sss`

## Bug Reporting Process

1. Record the defect in the team tracking system.
2. If the bug blocks progress, add it to [BLOCKERS.md](/home/edward/Development/MagnetarPrometheus/BLOCKERS.md).
3. Reflect impact in [STATUS.md](/home/edward/Development/MagnetarPrometheus/STATUS.md) when material.
4. Log key diagnosis and resolution steps in [BITACORA.md](/home/edward/Development/MagnetarPrometheus/BITACORA.md).
