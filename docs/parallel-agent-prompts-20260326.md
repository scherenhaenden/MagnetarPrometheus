# Parallel Agent Prompt Pack

This file is intentionally disposable. It exists to coordinate 10 parallel agents against the current MagnetarPrometheus repository state.

Repository root:

- `MagnetarPrometheus/`

Important current branches:

- `master`
- `implement-core-runtime-17609737249557533045`
- `review-runtime-remediation-20260326`

Current reality to preserve:

- The repository follows the Magnetar canonical governance model but is not the canonical model repository itself.
- The current prompt-scope completion is assessed at roughly 84 percent.
- The backend PoC runtime currently works through:
  - `scripts/bootstrap_python.sh`
  - `scripts/run_backend.sh`
  - `scripts/run_tests.sh`
- The implemented backend and SDK test scope currently passes with 100 percent coverage.
- The largest remaining gap is still the future UI graph model and shared workflow/editor contract.

Rules for every agent:

1. Read the governance and architecture markdowns first.
2. Follow the repository rules in `RULES.md`.
3. Keep changes small, coherent, and within your assigned scope.
4. Do not undo or rewrite work outside your scope.
5. Update `BITACORA.md`, `PLAN.md`, and `STATUS.md` only if your scope clearly requires it.
6. If you introduce new files, keep them modular and aligned with backend/sdk/ui boundaries.
7. Prefer code that is testable and keep or improve the existing coverage discipline.
8. If your work changes user-visible behavior or developer workflow, document it clearly.
9. If you touch runtime or contract behavior, add or update tests.
10. Before finishing, run only the smallest relevant validation for your scope.

Mandatory reading set for every agent:

- `README.md`
- `PocPlan.md`
- `RULES.md`
- `PLAN.md`
- `STATUS.md`
- `BITACORA.md`
- `ARCHITECTURE.md`
- `REQUIREMENTS.md`
- `docs/branch-review-core-runtime.md`

Shared validation context:

- Bootstrap path: `bash scripts/bootstrap_python.sh`
- Backend run path: `bash scripts/run_backend.sh`
- Test path: `bash scripts/run_tests.sh`

The prompts below are intentionally narrow and detailed.

---

## Agent 1: Backend CLI Entrypoint Hardening

### Objective

Replace the shell-only backend launch path with a proper Python CLI entrypoint while preserving `scripts/run_backend.sh` as a thin wrapper.

### Read First

- all mandatory reading files listed above
- `scripts/run_backend.sh`
- `backend/src/magnetar_prometheus/core/engine.py`
- `backend/src/magnetar_prometheus/core/workflow_loader.py`
- `backend/src/magnetar_prometheus/example_module.py`
- `backend/src/magnetar_prometheus/example_workflow.yaml`

### Scope

- create a Python entrypoint module under `backend/src/magnetar_prometheus/`
- allow it to run the current example workflow cleanly
- keep shell script behavior working by delegating to the Python entrypoint
- do not redesign the whole engine

### Deliverables

- Python CLI/entrypoint module
- updated `scripts/run_backend.sh`
- tests for the entrypoint behavior if practical
- minimal doc updates if command usage changes

### Constraints

- do not add unrelated command-line complexity
- keep the example workflow path explicit and easy to understand
- preserve current successful runtime output

### Validation

- `bash scripts/run_backend.sh`

---

## Agent 2: Bootstrap Policy And Error Handling

### Objective

Refine the dependency/bootstrap logic so missing dependencies and auto-install policy are explicit, structured, and configurable instead of mostly print-driven.

### Read First

- all mandatory reading files
- `backend/src/magnetar_prometheus/bootstrap.py`
- `scripts/bootstrap_python.sh`
- `backend/tests/test_bootstrap.py`
- `backend/tests/test_bootstrap2.py`

### Scope

- improve Python-side bootstrap behavior only
- introduce minimal structured errors or result objects if justified
- introduce a minimal policy switch or config mechanism for `auto_install`
- keep shell script changes minimal and only if required

### Deliverables

- cleaner bootstrap logic
- expanded tests for success, manual-only, install-failed, and disallowed-install paths
- small documentation note if the policy surface changes

### Constraints

- do not build a giant config system
- keep domain logic separate from dependency bootstrap logic
- preserve testability

### Validation

- smallest relevant bootstrap tests
- then `bash scripts/run_tests.sh`

---

## Agent 3: Workflow Schema And SDK Contract Strengthening

### Objective

Strengthen the shared SDK models so they better support both the backend runtime and future visual workflow tooling.

### Read First

- all mandatory reading files
- `sdk/python/src/magnetar_prometheus_sdk/models.py`
- `sdk/python/tests/test_models.py`
- `backend/src/magnetar_prometheus/example_workflow.yaml`
- relevant workflow sections in `PocPlan.md`

### Scope

- improve shared models only
- add carefully chosen supporting models if needed
- keep backward compatibility with the current backend slice where feasible
- prepare for future graph/editor work without implementing the UI

### Deliverables

- improved SDK models
- tests covering the new contract surface
- minimal updates to backend usage if required

### Constraints

- do not move UI code into sdk
- do not introduce speculative complexity with no current consumer
- keep naming neutral and portable

### Validation

- sdk model tests
- full test suite if backend usage changes

---

## Agent 4: Engine Next-Step Resolution Cleanup

### Objective

Harden the engine’s next-step resolution logic and make it more explicit, testable, and maintainable.

### Read First

- all mandatory reading files
- `backend/src/magnetar_prometheus/core/engine.py`
- `backend/tests/test_engine.py`
- next-step rules described in `PocPlan.md`

### Scope

- refactor only next-step and evaluation-related behavior
- clarify precedence between `next_step`, direct `next`, conditional branches, and terminal completion
- keep the current PoC semantics intact or improve them carefully

### Deliverables

- cleaner resolution logic
- better isolated evaluation helper(s)
- stronger test coverage for edge cases

### Constraints

- do not redesign the entire engine loop
- do not introduce unsafe `eval`
- preserve reproducibility

### Validation

- engine-focused tests
- then full test suite if needed

---

## Agent 5: Example Module Restructuring Toward Real Modules

### Objective

Move the current example flow toward the module structure envisioned in `PocPlan.md` without overengineering it.

### Read First

- all mandatory reading files
- `backend/src/magnetar_prometheus/example_module.py`
- `backend/src/magnetar_prometheus/example_workflow.yaml`
- module structure examples in `PocPlan.md`

### Scope

- reorganize the example flow toward a clearer module boundary
- keep the current example runnable
- if useful, introduce a minimal manifest or more realistic module folder layout inside backend

### Deliverables

- improved example module organization
- preserved runtime behavior
- updated tests for the new layout

### Constraints

- keep this a PoC, not a full plugin platform
- avoid breaking `scripts/run_backend.sh`
- avoid touching unrelated engine internals

### Validation

- example-related tests
- backend run script

---

## Agent 6: CI Workflow Quality Pass

### Objective

Improve the current GitHub Actions setup so CI is clearer, more robust, and better aligned with the repository’s actual run/test flow.

### Read First

- all mandatory reading files
- `.github/workflows/ci.yml`
- `.github/workflows/release.yml`
- `scripts/bootstrap_python.sh`
- `scripts/run_tests.sh`

### Scope

- refine CI and release workflow YAML only
- improve clarity, job naming, ordering, caching, or separation if justified
- keep the workflows simple and maintainable

### Deliverables

- improved CI workflow
- improved release metadata workflow if needed
- no unrelated code changes unless strictly necessary

### Constraints

- do not create a giant deployment pipeline
- align with the actual scripts and current Python PoC
- keep timestamp-based versioning intact

### Validation

- YAML sanity by inspection
- local script paths still valid

---

## Agent 7: Testing Discipline And Coverage Configuration Cleanup

### Objective

Clean up the testing/configuration layer so the 100 percent coverage rule is explicit, maintainable, and less shell-dependent.

### Read First

- all mandatory reading files
- `backend/pyproject.toml`
- `sdk/python/pyproject.toml`
- all current backend and sdk test files
- `scripts/run_tests.sh`

### Scope

- focus on test configuration and test quality
- remove brittle assumptions if found
- improve organization where it helps maintainability

### Deliverables

- cleaner pytest/coverage configuration
- test cleanup or consolidation where justified
- no scope creep into unrelated features

### Constraints

- preserve current 100 percent coverage
- do not reduce test strictness
- do not rewrite working runtime logic just for style

### Validation

- `bash scripts/run_tests.sh`

---

## Agent 8: Versioning And Release Stamp Surface

### Objective

Make the canonical timestamp versioning rule more explicit in the codebase and delivery surface, without pretending full semantic release automation exists.

### Read First

- all mandatory reading files
- `RULES.md`
- `ARCHITECTURE.md`
- `.github/workflows/release.yml`
- all places where `version` appears in the repo

### Scope

- clarify how the timestamp version stamp is produced and where it applies
- add a tiny helper, script, or documentation artifact if appropriate
- keep workflow definitions and package versions logically separate

### Deliverables

- more explicit version-stamp handling
- minimal docs or helper code/scripts as needed
- no fake release process beyond what the repo can actually support

### Constraints

- do not break package metadata
- do not replace workflow definition versions with release timestamps blindly
- keep the distinction between product/version metadata layers clear

### Validation

- verify release metadata path still makes sense

---

## Agent 9: UI Graph Model Specification Seed

### Objective

Create the first serious shared specification for future drag-and-drop workflow editing, without implementing the UI itself.

### Read First

- all mandatory reading files
- `ui/README.md`
- `sdk/schemas/README.md`
- relevant UI/workflow sections in `PocPlan.md`

### Scope

- define the first graph-model concept for nodes, edges, and editable workflow metadata
- keep it documentation-first or schema-first
- ensure it can map back to the current workflow execution model

### Deliverables

- a markdown spec or schema draft under `sdk/schemas/` or `docs/`
- explicit mapping between graph concepts and runtime workflow concepts
- minimal, high-signal tests only if code/schema tooling is introduced

### Constraints

- do not build the frontend
- do not overfit to one JS library
- keep the graph model compatible with the current backend PoC direction

### Validation

- consistency review against current backend workflow model

---

## Agent 10: Governance Truthfulness And Progress Accounting Pass

### Objective

Audit the governance markdowns so they remain truthful, current, and aligned with the real executable state of the repo.

### Read First

- all mandatory reading files
- `docs/branch-review-core-runtime.md`

### Scope

- review `PLAN.md`, `STATUS.md`, and `BITACORA.md`
- ensure task states, percentages, and claims match actual repository reality
- improve wording where the docs are too optimistic or too vague

### Deliverables

- cleaner planning/status/logbook alignment
- no inflated completion claims
- explicit remaining risks and next focus areas

### Constraints

- do not invent work that did not happen
- do not rewrite historical entries
- corrections belong in new log entries, not by erasing history

### Validation

- consistency check only
- no need to run runtime/tests unless your changes touch executable behavior

---

## Coordination Guidance

These prompts are designed to be parallelizable because each agent has a narrow ownership slice:

- Agent 1: CLI entrypoint
- Agent 2: bootstrap policy
- Agent 3: shared models
- Agent 4: engine next-step logic
- Agent 5: example module layout
- Agent 6: CI/release workflows
- Agent 7: tests/config
- Agent 8: versioning surface
- Agent 9: UI graph specification
- Agent 10: governance truthfulness

If multiple agents run simultaneously:

- avoid overlapping edits unless necessary
- prefer docs/spec work to stay separate from runtime code edits
- merge engine and test changes carefully because Agents 4 and 7 may interact
- merge bootstrap and CI changes carefully because Agents 2 and 6 may interact
