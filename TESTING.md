# Testing Strategy for MagnetarPrometheus

## Types Of Tests

- Unit tests for domain models, validation, next-step resolution, and executor routing
- Integration tests for full workflow execution using mock modules
- Contract tests for shared SDK/schema compatibility between backend and UI-facing payloads
- Future end-to-end tests for visual workflow creation and serialization

## Code Coverage

- Backend automated test target: at least 80% coverage on core orchestration code
- Shared schema validation target: all schema transformations covered by tests

## Acceptance Criteria

- A sample workflow can load, execute, branch, and produce a deterministic context output
- Invalid workflow definitions fail validation clearly
- Shared schema artifacts can round-trip between editor-facing and runtime-facing representations

## Bug Reporting Process

1. Record the defect in the team tracking system.
2. If the bug blocks progress, add it to [BLOCKERS.md](/home/edward/Development/MagnetarPrometheus/BLOCKERS.md).
3. Reflect impact in [STATUS.md](/home/edward/Development/MagnetarPrometheus/STATUS.md) when material.
4. Log key diagnosis and resolution steps in [BITACORA.md](/home/edward/Development/MagnetarPrometheus/BITACORA.md).

