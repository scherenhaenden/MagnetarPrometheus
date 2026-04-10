# Status of MagnetarPrometheus

## Executive Summary

MagnetarPrometheus currently has a working backend proof of concept, not a finished end-user application.

What is real today:

- A Python workflow engine can load a YAML workflow, execute registered steps, evaluate conditional routing, and return a structured `RunContext`.
- A bootstrap path can prepare the local Python runtime and install the dependencies required by the current proof-of-concept slice.
- A one-command local launcher exists: `bash run_app.sh`.
- The local API server can now also be managed through repo-root daemon lifecycle commands.
- An example workflow, `email_triage`, runs end to end and produces deterministic JSON output.
- CI and local test execution enforce `100%` coverage for the implemented backend and SDK scope.
- The Angular UI tier now also enforces `100%` coverage for statements, branches, functions, and lines.

What is not real yet:

- There is no production-grade long-running backend service with persistence, queueing, or worker management.
- There is no complete HTTP API for job submission or run inspection.
- A first Angular web shell exists in mock mode (`ui/`), upgraded to Angular 21, but it is not API-backed yet.
- There is no desktop UI.
- There is no operator dashboard, queue manager, or persistent run history.
- There is no production-grade release/publishing pipeline beyond metadata/version-stamp generation.

So the product state is best described as:

- backend execution core: present
- shared schema boundary: present
- visual/editor product surface: not implemented yet
- operational product surface: not implemented yet

## Current Product Reality

If a user runs:

```bash
bash run_app.sh
```

the repository will:

1. bootstrap the local Python environment
2. load the example workflow from `backend/src/magnetar_prometheus/modules/email_module/email_triage.yaml`
3. execute that workflow through the backend engine
4. print the resulting workflow state as JSON
5. exit

That means the current user experience is primarily batch-style CLI execution, with a minimal local API mode available for development and validation.

## What A User Can Do Right Now

- Run the current proof-of-concept workflow engine locally from the repository root.
- Execute the built-in example workflow and inspect the final workflow state.
- Point the CLI at another compatible workflow YAML file.
- Start, stop, and inspect the status of the minimal local API server from the repository root.
- Inspect how the engine resolves steps, branching, evaluator logic, and context aggregation.
- Validate changes through the local test path and CI-oriented scripts.

## What A User Cannot Do Yet

- Create workflows through a visual editor.
- Drag and drop nodes in a UI.
- Submit jobs to a persistent runtime service.
- Browse previous runs in a dashboard.
- Manage installed modules through an application surface.
- Run a hosted or desktop application experience.

## Progress Summary

The tracked planning baseline is marked complete for the currently defined `44 / 44` effort points, but that does not mean the overall product vision is complete. It means the currently scoped foundation/runtime/schema milestones are complete. A new planning baseline (`ms-04`, `ms-05`) is now established to move from the completed CLI PoC to a visible app surface.

- Active scoped completion: `100%` (`44 / 44` effort points)
- Historical governance-audit view preserved: `84%` prompt-scope completion, `19 / 44` effort points fully completed at that time
- Historical merged-branch view preserved: `89%` (`39 / 44` effort points) at that time

```text
[####################] 100% of the currently defined baseline
```

## Current Milestones

- `ms-01` Foundation Setup: Completed
  Meaning: the repository structure, governance files, and versioning/testing conventions exist.
- `ms-02` Core Runtime PoC: Completed
  Meaning: a backend runtime can execute a sample workflow through the CLI.
- `ms-03` Visual Model Baseline: Completed
  Meaning: the shared graph/schema boundary is defined, not that a workflow editor already exists.
- `ms-04` Service API & Persistence: Planned
  Meaning: a long-running backend service can accept job submissions via an HTTP API, queue runs, and write persistent run history.
- `ms-05` Minimal Web UI: Planned
  Meaning: a user-facing web UI can fetch and display run history and workflow details.

## Implemented Capabilities

- Workflow loading from YAML through the backend loader.
- Serial workflow execution with step-by-step context accumulation.
- Conditional routing through the evaluator path.
- Step registration and Python executor routing.
- Structured context/result output for completed runs.
- Example email-triage module with manifest, workflow, and step handlers.
- Runtime bootstrap with dependency checking and policy-driven install behavior.
- Local scripts for bootstrap, run, and test flows.
- Canonical version-stamp generation for release metadata.
- High-coverage automated tests for the current backend and SDK slice.

## Important Limitations

- The runtime is invoked per command and exits after the workflow completes.
- There is no scheduler, queue, or worker pool.
- Workflow definitions are still authored manually rather than through a product interface.
- The UI graph schema is a contract artifact only; it is not backed by a functioning editor.
- The current module surface is demonstrative, not yet a mature plug-and-play module system.
- Release automation currently produces metadata/version-stamp outputs, not a complete distribution pipeline.

## Immediate Delivery Focus

- Begin execution on the HTTP API and minimal Web UI slices to introduce a visible application surface.
- Deliver a long-running execution surface instead of only one-shot CLI execution.
- Make workflow submission, inspection, and result viewing understandable without reading source code.
- Keep the UI graph schema aligned with runtime semantics while the first actual UI slice is built.
- Keep work user-incremental so each round gives the user one more thing to test directly.

## Risks And Mitigations

- Risk: the project reports “complete” against the current plan while still feeling incomplete to end users
  Mitigation: describe completion as “baseline scope complete” and document the missing product layers explicitly.

- Risk: workflow runtime and visual graph model diverge early
  Mitigation: keep shared contracts in `sdk/` as the boundary between runtime and future UI.

- Risk: backend-first implementation hardcodes Python assumptions into workflow definitions
  Mitigation: continue separating runtime internals from shared workflow/schema contracts.

- Risk: users expect an app surface when only a CLI execution slice exists
  Mitigation: state plainly in the docs that the current deliverable is a backend proof of concept, not a finished interactive product.

## Frontend Packet Progress (11 → 20)

- Snapshot date: **2026-04-07**
- Estimated completion: **100% (within scoped packet definitions)**

| Packet | Status | Completion |
| --- | --- | --- |
| 11 | Prompt index/orchestration | 100% |
| 12 | Workspace skeleton | 100% |
| 13 | Web shell | 100% |
| 14 | Data contract boundary (mock+api) | 100% |
| 15 | Design system/layout primitives | 100% |
| 16 | Run history + run detail slice | 100% |
| 17 | Job submission slice | 100% |
| 18 | Desktop shell skeleton | 100% |
| 19 | Frontend testing + doc guards | 100% |
| 20 | Frontend local run flow | 100% |

Residual constraint: some Codex sandbox environments cannot bind Karma's local port `9876`, so local browser-test failures there should not be confused with the actual repository coverage policy. On a normal developer machine and in GitHub Actions, the UI tier now runs with explicit `100%` coverage enforcement.

## CI and Release Automation

The repository has active GitHub Actions automation under `.github/workflows/`.

### CI Workflow (`ci.yml`)

Triggers on every push to `master`/`main` and on every pull request targeting those branches.

Steps enforced:
1. **Runtime toolchain setup** — installs Python `3.11`, Node `22.12.0`, and the UI dependencies from `ui/package-lock.json` so both backend and Angular validation paths run against declared toolchain versions.
2. **Bootstrap validation** — runs `scripts/bootstrap_python.sh` to verify a clean environment can be prepared.
3. **Backend run-path validation** — runs `scripts/run_backend.sh` (no extra arguments) to verify the example workflow loads and executes end to end.
4. **Test execution with coverage enforcement** — runs `scripts/run_tests.sh` which invokes `pytest` for the backend and SDK scope, then the implemented UI validation tier. Backend coverage remains enforced via the threshold in `backend/pyproject.toml`, and the Angular UI tier now enforces `100%` coverage through `ui/karma.conf.cjs`.

### Release Metadata Workflow (`release.yml`)

Triggers on push to `master`, on `release-*` tags, or manually via `workflow_dispatch`.

- Generates a canonical version stamp in the format `yyyy.MM.dd HH:mm:ss.SSS`.
- Uploads `release-version.txt` as a GitHub Actions artifact.
- Does NOT create git tags, GitHub releases, or publish packages. Full publishing is out of scope at the current PoC stage.

### Automation Status

- CI automation: **active and enforced**.
- Release metadata generation: **active**.
- Full distribution/publishing pipeline: **not implemented** (out of scope for current PoC).

## Operating Rhythm

- Update this file when product reality changes, not only when task states change.
- Always describe both implemented capability and current limitation.
- Map implementation work to GitHub issues and broader product/architecture questions to GitHub discussions.
