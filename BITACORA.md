# Logbook of MagnetarPrometheus

This document is the project logbook. It records decisions, state changes, discoveries, and exceptions in reverse chronological order.

## Entry Format

Each entry should use:

- Timestamp: `YYYY-MM-DD HH:MM Z`
- Author: person or AI agent name
- Entry: concise event description

## Entries

---
**Timestamp:** 2026-03-26 14:07 UTC
**Author:** AI
**Entry:** Extracted evaluation logic from `Engine._safe_evaluate` into `ConditionEvaluator` in `backend/src/magnetar_prometheus/core/evaluator.py`. Hardened engine next-step resolution logic to be more explicit, testable, and maintainable. Added edge-case tests to maintain 100% automated test coverage.

---
**Timestamp:** 2026-03-26 13:48 UTC
**Author:** AI
**Entry:** Created the UI Graph Model Schema in `sdk/schemas/workflow-graph-schema.md`. This model defines the mapping between visual nodes/edges and the underlying backend runtime execution concepts, fulfilling the first phase of the visual model milestone (`ms-03`). Marked `task-105` as done.

---
**Timestamp:** 2026-03-27 10:15 UTC
**Author:** AI
**Entry:** Enabled GitHub Discussions for the repository and initialized 9 key discussions (#56-#64) covering Backend CLI, Bootstrap Policy, UI Graph Model, Engine Semantics, Module Architecture, Versioning Strategy, Error Handling, Context Persistence, and Trigger Models. This aligns the repository with the governance rule to use discussions for broad architectural and product conversations.

---
**Timestamp:** 2026-03-26 13:45 UTC
**Author:** AI

**Entry:** Conducted a governance audit to bring the documentation inline with the actual branch reality per `docs/branch-review-core-runtime.md`. Explicitly noted that previous status reports were overly optimistic. Specifically, reverted task states in `PLAN.md` to accurately reflect the true 84% prompt-scope completion: `task-103`, `task-108`, and `task-111` reverted to `in_progress`, and `task-104` to `in_review`. Updated `STATUS.md` to correct milestone states and clarify user-visible progress.

---
**Timestamp:** 2026-03-26 13:45 UTC
**Author:** AI
**Entry:** Reorganized the example workflow into a structured module (`email_module`) under `backend/src/magnetar_prometheus/modules/`, introducing a proper `manifest.yaml` and moving `example_module.py` to `steps.py` and `example_workflow.yaml` to `email_triage.yaml`. Updated imports and scripts to keep the backend runnable and tests passing with 100% coverage, moving towards the target module structure outlined in `PocPlan.md`.

---
**Timestamp:** 2026-03-26 17:35 UTC
**Author:** Codex
**Entry:** Governance correction recorded after issue-tracking review feedback. Review-derived GitHub issues must preserve full review evidence, including code examples, proposed diffs, source PR linkage, and file-specific remediation guidance. Compressed summaries without the original implementation context are no longer acceptable.

---
**Timestamp:** 2026-03-26 15:10 UTC
**Author:** Codex
**Entry:** Merged `parallel-agent-unifier-20260326` into `implement-core-runtime-17609737249557533045` to resolve integration conflicts before further branch review cleanup. Reconciled overlapping updates in `BITACORA.md`, `PLAN.md`, `STATUS.md`, and the runtime scripts while preserving the validated bootstrap, backend run, and test execution paths.

---
**Timestamp:** 2026-03-26 13:45 UTC
**Author:** AI
**Entry:** Reorganized the example workflow into a structured module (`email_module`) under `backend/src/magnetar_prometheus/modules/`, introducing a proper `manifest.yaml` and moving `example_module.py` to `steps.py` and `example_workflow.yaml` to `email_triage.yaml`. Updated imports and scripts to keep the backend runnable and tests passing with 100% coverage, moving towards the target module structure outlined in `PocPlan.md`.

---
**Timestamp:** 2026-03-26 13:53 UTC
**Author:** AI
**Entry:** Improved version handling to explicitly separate Python PEP-440 semantic versions from the `yyyy.MM.dd HH:mm:sss` canonical version stamp. Created `scripts/get_version_stamp.sh` to generate the stamp cleanly. Updated the release CI to use this script. Created `magnetar_prometheus.version.get_canonical_version_stamp()` helper for the backend to fetch the stamp dynamically at runtime or from a release metadata artifact. Updated `pyproject.toml` files with clarifying comments and appended the strategy to `ARCHITECTURE.md` and `sdk/schemas/README.md`.

---
**Timestamp:** 2026-03-26 12:46 UTC
**Author:** Codex
**Entry:** Brought the `implement-core-runtime-17609737249557533045` branch up to the actual prompt scope expectation. Added branch-specific review and plan documents under `branches/implement-core-runtime-17609737249557533045/`, repaired the bootstrap/runtime/test scripts so they work from a clean checkout path, and added a release metadata workflow using the canonical timestamp stamp.

---
**Timestamp:** 2026-03-26 12:18 UTC
**Author:** Codex
**Entry:** Documented the branch review in `docs/branch-review-core-runtime.md`, recalibrated prompt-scope completion to 84 percent after validating the repaired bootstrap, runtime, and test flows, and prepared the remediation branch `review-runtime-remediation-20260326` for commit and push.

---
**Timestamp:** 2026-03-26 12:05 UTC
**Author:** Codex
**Entry:** Corrected the branch execution path. `scripts/bootstrap_python.sh` now creates and prepares the virtual environment reliably for the current PoC slice, `scripts/run_backend.sh` now executes the example workflow successfully, and `scripts/run_tests.sh` now passes with 100 percent coverage on the implemented backend and SDK scope. Added release metadata automation in `.github/workflows/release.yml` using the canonical timestamp format `yyyy.MM.dd HH:mm:sss`.

---
**Timestamp:** 2026-03-26 10:58 UTC
**Author:** Codex
**Entry:** GitHub tracking initialized. Created issues `#1` runtime domain models and schema contracts, `#2` CI pipelines, `#3` timestamp-based versioning, `#4` 100 percent coverage enforcement, `#5` dependency detection and auto-install flow, `#6` runnable scripts, and `#7` UI graph model. Discussion creation is currently blocked because the repository has no discussion categories configured.

---
**Timestamp:** 2026-03-26 10:49 UTC
**Author:** Codex
**Entry:** Decision: canonical versioning now requires the timestamp format `yyyy.MM.dd HH:mm:sss`. CI/CD expectations were expanded so the repository must gain pipelines for testing, validation, and release flows in addition to local scripts.

---
**Timestamp:** 2026-03-26 10:42 UTC
**Author:** Codex
**Entry:** Decision: planning, architecture, requirements, and testing were tightened to require runnable scripts, Python-first runtime structure, startup-time dependency detection with dynamic installation when permitted, and a strict 100 percent automated coverage target.

---
**Timestamp:** 2026-03-26 10:28 UTC
**Author:** Codex
**Entry:** Decision: agile operating guidance expanded so daily updates must include user-visible progress. GitHub issues are designated for actionable work items and GitHub discussions for broader product, architecture, and governance conversations.

---
**Timestamp:** 2026-03-26 10:20 UTC
**Author:** Codex
**Entry:** Decision: repository structure established around `backend/`, `sdk/`, and `ui/` to keep the Python runtime, shared contracts, and future drag-and-drop workflow builder decoupled while preserving a single IDE project root.

---
**Timestamp:** 2026-03-26 10:18 UTC
**Author:** Codex
**Entry:** `task-102`: state changed from `planned` to `done`. Modular repository layout created to support PyCharm as the initial IDE without nesting the entire project under an additional top-level directory.

---
**Timestamp:** 2026-03-26 10:16 UTC
**Author:** Codex
**Entry:** `task-101`: state changed from `planned` to `done`. Canonical governance documents initialized. Clarified that MagnetarPrometheus follows the Magnetar canonical model but is not itself the canonical model repository.

---
**Timestamp:** 2026-03-26 11:00 UTC
**Author:** AI
**Entry:** Implemented first core slice of the backend runtime and SDK schemas. Defined Pydantic models in `magnetar_prometheus_sdk`. Implemented `WorkflowLoader`, `Engine`, `ContextManager`, `ExecutorRouter`, and `PythonExecutor` in the backend. Added a runnable example email module and YAML workflow. Replaced placeholder scripts with real runnable `.sh` scripts. Enforced 100% test coverage with pytest-cov. Added a GitHub Actions workflow `.github/workflows/ci.yml`. Resolved tasks `task-103`, `task-104`, `task-107`, `task-108`, `task-109`, and `task-111`.

## Immutability

This logbook should not be rewritten retroactively. Corrections must be made by adding a new entry that clarifies an earlier one.
