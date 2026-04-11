# Logbook of MagnetarPrometheus

<!--
Why this file exists in this form:

- This file is the canonical reverse-chronological project logbook. It is not a changelog,
  not a release note file, and not a narrative diary. Its job is to preserve decisions,
  conflict resolutions, branch reconciliations, governance corrections, and important
  implementation state transitions in a format that can be scanned quickly later.
- Entries are intentionally concise and structured because this document is meant to be
  updated often across many branches and merge events. The stable Timestamp / Author /
  Entry shape reduces ambiguity during merges and makes historical reconstruction easier
  for both humans and automation.
- Reverse chronological order is deliberate. The newest operational truth needs to be at
  the top so an engineer or agent opening the file can understand the latest state before
  reading older history that may already have been superseded.
- References to GitHub issues, pull requests, workflows, and branch names are kept inline
  because this file acts as the bridge between repository state and repository process.
  When a branch, PR, or issue drove a change, this file should make that linkage obvious.
- This file should preserve meaningful operational context, not every tiny edit. The bar
  for an entry is that it helps explain why the repository looks the way it does, why a
  conflict was resolved a certain way, or what higher-level work a set of commits served.
- If this file ever starts to look like a wall of repetitive low-signal notes, the right
  fix is not to remove structure but to tighten entry discipline so only decisions and
  notable state changes remain.
-->

This document is the project logbook. It records decisions, state changes, discoveries, and exceptions in reverse chronological order.

## Entry Format

Each entry should use:

- Timestamp: `YYYY-MM-DD HH:MM Z`
- Author: person or AI agent name
- Entry: concise event description

## Entries

---
**Timestamp:** 2026-04-11 11:58 CEST
**Author:** Codex
**Entry:** Cerré el último pase de PR `#179` en `codex/redisenar-interfaz-y-funcionalidad-del-menu`. Ajusté `WorkflowStudioPageComponent` para responder a los reviews finales: tabs con botón de cierre accesible como control hermano, restauración real del draft al volver a la pestaña Draft, actualización inmutable de `openProjectTabs`, conexiones calculadas con `Map` y constantes descriptivas, y cobertura dirigida para ese comportamiento. Verificado con `npm run test:ci`: 103/103 tests UI en verde y 100.00% en statements, branches, functions y lines.

---
**Timestamp:** 2026-04-10 18:30 CEST
**Author:** Gemini CLI
**Entry:** Modernized the Workflow Studio UI to use Angular 21 standards, replacing all legacy `*ngIf` and `*ngFor` directives with the newer `@if` and `@for` control flow syntax. Refactored the workflow execution simulation in `WorkflowStudioPageComponent` to use an RxJS-based engine (`from`, `concatMap`, `delay`) for better robustness and cancellation support. Hardened the node drag interaction with early `event.preventDefault()` calls to prevent default browser behaviors. Improved the `run_app.sh` daemon manager by strengthening the process termination loop with a verified SIGKILL fallback. Updated the UI test suite to maintain 100% code coverage. Linked PR 177 to Issue #155.

---
**Timestamp:** 2026-04-10 18:00 CEST
**Author:** Codex
**Entry:** Cerré la brecha de pruebas que quedaba en `codex/add-example-workflow-display` para que la integración del Workflow Studio con el navegador de ejemplos no rebajara el estándar del repositorio. Añadí cobertura específica sobre persistencia local, carga de ejemplos con respuestas stale, generación de IDs, drag state, ejecución/stop del flujo, y ramas defensivas de storage y nombres vacíos. Verificado con `npm run test:ci`: 104/104 tests UI en verde y 100.00% en statements, branches, functions y lines.

---
**Timestamp:** 2026-04-10 14:25 CEST
**Author:** Codex
**Entry:** Resolved the active merge on `codex/add-example-workflow-display` by integrating the example-workflow browser into the newer Workflow Studio shell instead of keeping two divergent page implementations. The merged result preserves the saved example asset tabs inside the current Studio canvas, adds ARIA tab semantics to the format switcher, replaces the example error hardcode with the semantic danger token, and hardens example loading against stale asynchronous responses so quick tab switches cannot overwrite the current preview with an older response.

---
**Timestamp:** 2026-04-10 17:00 CEST
**Author:** Gemini CLI
**Entry:** Hardened Workflow Studio UX and Accessibility on branch `codex/improve-ui-design-and-theme-options` (PR `#174`). Addressed review feedback by implementing `dragPointerId` tracking, a 5px drag threshold, and boundary clamping to ensure robust and predictable node movement. Enhanced accessibility with `tabindex`, `role="button"`, and keyboard handlers for node selection. Improved visual stacking with dynamic `z-index` during dragging. Maintained 100.00% statement and branch coverage with 110 total UI tests.

---
**Timestamp:** 2026-04-10 16:40 CEST
**Author:** Gemini CLI
**Entry:** Merged `codex/redesign-application-ui-using-provided-react-design` into `codex/improve-ui-design-and-theme-options` (PR `#174`). Resolved significant conflicts in `WorkflowStudioPageComponent` across CSS, HTML, and TypeScript, successfully integrating theme options and accent selectors with the recently added local project persistence and editing features. Expanded UI unit tests to 108 total specs, covering new theme state and drag-and-drop logic to maintain 100.00% statement, branch, and line coverage. Verified all 118 backend and 108 UI tests pass.

---
**Timestamp:** 2026-04-10 16:15 CEST
**Author:** Gemini CLI
**Entry:** Finalized PR `#175` hardening pass. Achieved 100.00% code coverage for both Backend and UI slices (fixing the prior Chrome Headless coverage failure). Extracted a shared `build_plugin_manager` bootstrap helper to remove duplication, hardened plugin discovery with defensive error handling and logging, and standardized hyphenation in core documentation. Verified all 118 backend and 102 UI tests pass with full branch and statement coverage. Updated PR description to reflect the improved technical baseline.

---
**Timestamp:** 2026-04-10 14:45 CEST
**Author:** Gemini CLI
**Entry:** Completed review follow-up for PR `#175`. Extracted `build_plugin_manager` to a shared bootstrap module to remove duplication across the CLI and API server. Hardened `PluginManager.discover_entrypoint_plugins` with robust error handling, type checks, and logging. Standardized "step-capability" hyphenation across `README.md`, `ARCHITECTURE.md`, and `STATUS.md`. Simplified the backward-compatible `register_all_example_steps` helper. All 118 backend tests pass with 100.00% total coverage.

---
**Timestamp:** 2026-04-10 14:15 CEST
**Author:** Gemini CLI
**Entry:** Restored 100% code coverage for the backend on branch `codex/plan-plugin-architecture-for-extensibility` (PR `#175`). Added missing test cases in `backend/tests/test_plugins.py` to cover `PluginManager` duplicate registration, entrypoint discovery (via monkeypatching), and step ownership diagnostics. Verified all 118 backend tests pass with 100.00% total coverage.

---
**Timestamp:** 2026-04-10 13:30 CEST
**Author:** Gemini CLI
**Entry:** Resolved UI code contract and build failures on `codex/add-functionality-to-save-and-load-workflows` to unblock PR `#176`. Added explicit `public` access modifiers to `ngOnInit` and `ngOnDestroy` in `WorkflowStudioPageComponent` as required by the repository's UI contract guard. Increased the `anyComponentStyle` budget in `ui/angular.json` to 10kb/20kb to accommodate the redesigned Workflow Studio styles. Verified the fixes by running the UI test tier: contract and build checks now pass. Updated PR `#176` with labels (`✨ feature`, `🎨 ux`, `🧪 tests`, `♻️ code quality`, `area:ui`, `Level 3 (Visual Model)`) and linked it to issue `#7`.

---
**Timestamp:** 2026-04-10 13:45 CEST
**Author:** Codex
**Entry:** Completed the remaining PR `#176` Workflow Studio review follow-up on `codex/add-functionality-to-save-and-load-workflows`. Saving an existing local project now moves it back to the top of the selector so the most recently updated snapshot stays easiest to reach, and storage access is now wrapped defensively so unavailable or failing browser storage degrades into explicit status messages instead of silently assuming persistence succeeded. Added focused specs for reorder-on-save plus failing read/write storage scenarios and updated the branch-local review record to mark the review items as closed in code.

---
**Timestamp:** 2026-04-10 13:25 CEST
**Author:** Codex
**Entry:** On `codex/add-functionality-to-save-and-load-workflows`, tightened Workflow Studio local-project persistence after PR `#176` review triage. Hardened project restore against corrupt `localStorage` entries such as `null`, switched project ID generation to `crypto.randomUUID()` with a compatibility fallback, and added focused specs covering both the corrupt-storage recovery path and the UUID generation path. Also recorded an explicit branch-local review in `branches/codex/add-functionality-to-save-and-load-workflows/review.md` so the remaining open review items stay visible.

---
**Timestamp:** 2026-04-10 11:55 CEST
**Author:** Codex
**Entry:** Hardened PR `#170` on `feature/add-example-workflows-10944637492021849479` by making the example math and HTTP steps preserve existing `context['data']` instead of overwriting it, guarding non-mapping context payloads in the math path, and replacing brittle JSON string interpolation in the HTTP mock with `json.dumps`. Expanded the module tests to cover preserved data fields, invalid/non-mapping context payloads, and special-character URL serialization. Verified the touched tests with `pytest --no-cov backend/tests/test_math_module.py backend/tests/test_http_module.py -q`: `12 passed`.

---
**Timestamp:** 2026-04-10 11:20 CEST
**Author:** Codex
**Entry:** On `codex/redesign-application-ui-using-provided-react-design`, hardened the Workflow Studio implementation after local compile/build investigation. Fixed the Angular template parse failure caused by literal JSON braces in the inspector preview, centralized node-sequence/state lookup in the component to avoid drift and repeated O(N) template work, restored explicit standalone component metadata for the lazy-loaded route target, and moved the redesigned Studio styling back onto repository design tokens instead of local hardcoded palette values.

---
**Timestamp:** 2026-04-09 15:25 CEST
**Author:** Codex
**Entry:** Tightened the Angular UI validation tier on branch `feature/add-ui-tests-12952883483010130617` so `npm run test:ci` now enforces `100%` statements/branches/functions/lines via `ui/karma.conf.cjs` instead of only requiring test green status. Closed the remaining coverage gaps by expanding route-loader, job-submission, run-detail, run-history, API-adapter, mock-adapter, and provider tests until the only remaining failures were true uncovered branches rather than missing policy wiring.

---
**Timestamp:** 2026-04-07 13:20 UTC
**Author:** Codex
**Entry:** Advanced the frontend packet stream from `11`/`12` toward `20` on branch `feature/frontend-11-20-progress` by replacing the Angular starter template with a routed shell, adding a documented frontend contract boundary (`FrontendDataService`) with a mock adapter, implementing run-history/run-detail and job-submission slices in mock mode, and updating `ui/README.md` plus packet docs with explicit completion percentages and pending gaps (notably packet `18` desktop shell and root-level UI tier automation integration).

---
**Timestamp:** 2026-04-02 16:23 CEST
**Author:** Codex
**Entry:** Resolved the pending cleanup set for issues `#111`, `#106`, `#109`, `#95`, and `#96` on the current branch. Reordered the misplaced `2026-03-26 11:00 UTC` Bitacora entry back into strict reverse chronology, hardened the email example step to fail cleanly when the first message lacks a subject, made the base executor contract raise `NotImplementedError` explicitly so the abstract test proves real behavior, escaped regex-sensitive `pytest.raises(match=...)` patterns, and aligned the canonical version stamp contract to the portable `yyyy.MM.dd HH:mm:ss.SSS` form across the shell script, backend helper, tests, and current normative docs.

---
**Timestamp:** 2026-04-02 16:00 CEST
**Author:** Codex
**Entry:** Addressed the last actionable PR `#153` audit concern by tightening `DependencySpec` validation in `backend/src/magnetar_prometheus/bootstrap.py` and documenting why the `pip install` subprocess call is not shell-interpolated: it uses argv-list form without `shell=True`. Added a focused bootstrap test so malformed blank dependency declarations now fail early and the bootstrap contract stays explicit.

---
**Timestamp:** 2026-04-02 15:41 CEST
**Author:** Codex
**Entry:** Added a split set of independent frontend/delegation prompts under `work-/for-agents/11-frontend-prompt-index.md` through `20-frontend-local-run-flow.md`. The prompts are Angular-only for the web surface, explicitly reject React, and are divided by disjoint ownership so workspace scaffolding, web shell, data boundary, design system, run-history slice, job-submission slice, desktop shell, validation guards, and local run flow can be delegated separately.

---
**Timestamp:** 2026-04-02 15:34 CEST
**Author:** Codex
**Entry:** Resolved the `master` merge on `copilot/add-dependency-installation-report` by preserving the branch's long-form bootstrap intent documentation while replacing the raw dependency dict contract in `backend/src/magnetar_prometheus/bootstrap.py` with an explicit `DependencySpec` dataclass. Updated the bootstrap regression tests to use the structured dependency type so the non-short-circuit installation guarantee remains covered without reverting to stringly-typed key access.

---
**Timestamp:** 2026-04-02 15:11 CEST
**Author:** Codex
**Entry:** Addressed the fourth actionable PR `#159` review fix by replacing the `parents[2]` repository-root assumption in `backend/tests/test_documentation_contract.py` with an upward search for stable repo markers (`BITACORA.md` and `backend/pyproject.toml`). The documentation-contract test is now less brittle if the test package layout moves later.

---
**Timestamp:** 2026-04-02 15:10 CEST
**Author:** Codex
**Entry:** Addressed the third actionable PR `#159` review fix by extending `backend/tests/test_documentation_contract.py` to protect the long policy comment above `DEFAULT_API_HOST` in `api/server.py`. The branch now treats that explanatory comment block as part of the enforced documentation contract instead of leaving it unguarded.

---
**Timestamp:** 2026-04-02 15:09 CEST
**Author:** Codex
**Entry:** Addressed the second actionable PR `#159` review fix by making `backend/tests/test_documentation_contract.py` target the specific CLI API-mode test docstrings through AST parsing instead of searching the entire file text. The documentation-contract guard remains strict, but it is now tied to the exact tests whose policy explanations it is meant to protect.

---
**Timestamp:** 2026-04-02 15:09 CEST
**Author:** Codex
**Entry:** Addressed the first actionable PR `#159` review fix by deriving the CLI `--host` help text from `DEFAULT_API_HOST` instead of hardcoding `127.0.0.1`. This keeps the operator-facing help text aligned with the centralized default host policy and prevents future drift between code behavior and CLI messaging.

---
**Timestamp:** 2026-04-02 14:48 CEST
**Author:** Codex
**Entry:** Added a documentation-contract test for the PR `#152` API/CLI surface so future cleanup passes cannot silently shrink the heavy intent comments below the repository's preferred threshold. Restored long-form rationale in `api/server.py`, `cli.py`, and `backend/tests/test_cli.py`, and wired the new validator into `scripts/run_tests.sh`.

---
**Timestamp:** 2026-04-02 14:48 CEST
**Author:** Codex
**Entry:** Addressed the remaining PR `#152` cleanup feedback by centralizing the default API loopback host in `api/server.py` and reusing it from the CLI, then trimming a few overly repetitive comments/docstrings in the CLI, API server, and CLI tests without weakening the documented security intent.

---
**Timestamp:** 2026-04-02 14:41 CEST
**Author:** Codex
**Entry:** Resolved the `master` merge on `copilot/fix-api-server-loopback-binding` by reconciling the CLI API-mode changes. The merged result keeps the branch's loopback-by-default and explicit `--host` forwarding while preserving the newer `master` startup-failure normalization and workflow-short-circuit test coverage.

---
**Timestamp:** 2026-04-02 14:18 CEST
**Author:** Codex
**Entry:** Addressed the substantive PR `#127` review finding by removing `branches/feature/planning-product-surface/plan.md`, which was only a branch-local achievement artifact. The durable planning state remains in `PLAN.md`, `STATUS.md`, and `ARCHITECTURE.md` rather than in a feature-branch documentation path.

---
**Timestamp:** 2026-04-02 14:16 CEST
**Author:** Codex
**Entry:** Resolved the `master` merge on `feature/planning-product-surface-7059919661031247844` by preserving the newer Bitacora-retention planning task from `master` as `task-112`, renumbering the product-surface planning tasks to `task-113` and `task-114`, and restoring strict reverse-chronological ordering at the top of the logbook.

---
**Timestamp:** 2026-04-02 14:10 CEST
**Author:** Codex
**Entry:** Addressed the last remaining PR `#121` governance-doc review item by adding a direct cross-reference from `RULES.md` to `WIP_GUIDELINES.md` for "disjoint write ownership" and by defining that term in a dedicated WIP-guidance section with a concrete example of safe parallel work partitioning.

---
**Timestamp:** 2026-04-02 14:05 CEST
**Author:** Codex
**Entry:** Addressed the second remaining PR `#121` governance-doc review item by rephrasing the `RULES.md` documentation-discipline requirement to match the repo's newer governance language in `CONTRIBUTING.md`. The rule now speaks consistently in terms of whether an increment is user-visible or internal-only instead of using the older "actually user-testable" phrasing.

---
**Timestamp:** 2026-04-02 14:03 CEST
**Author:** Codex
**Entry:** Addressed the last remaining PR `#121` wording nit by making `WIP_GUIDELINES.md` enforce user-incremental delivery with mandatory language rather than optional phrasing. The guidance now states that each round must leave something runnable, visible, or inspectable and that work packets must unlock a small user-visible or user-testable increment.

---
**Timestamp:** 2026-04-02 14:00 CEST
**Author:** Codex
**Entry:** Merged current `master` into `chore/governance-user-incremental-16392512902076639900` before finishing the PR `#121` review pass. Preserved the branch's governance additions around disjoint write ownership, user-visible versus internal-only reporting, and the meaning of `done`, while also keeping the newer repository-wide documentation standards that later landed on `master`.

---
**Timestamp:** 2026-04-02 13:55 CEST
**Author:** Codex
**Entry:** Addressed the first remaining PR `#121` governance-doc review item by splitting the `RULES.md` `in_review` to `done` transition note into a short main bullet plus a separate clarification line. This keeps the rule visible while making the caution about internal-only completion easier to scan during reviews.

---
**Timestamp:** 2026-04-02 13:50 UTC
**Author:** GitHub Copilot (Coding Agent)
**Entry:** Stabilised CI/release pipeline automation on branch `copilot/create-ci-pipelines-for-testing`. Added substantial RULES.md-required comment headers to `.github/workflows/ci.yml` and `.github/workflows/release.yml` describing intent, validated execution paths, and non-obvious semantics (step ordering rationale, server-mode non-activation, coverage threshold centralisation, PoC-scope publishing exclusion). Updated `STATUS.md` with an explicit "CI and Release Automation" section covering the active workflows, their trigger conditions, steps enforced, and current automation limits. This completes the documentation alignment required by the issue acceptance criteria.

---
**Timestamp:** 2026-04-02 12:15 CEST
**Author:** Gemini CLI
**Entry:** Completed PR `#122` on branch `feature/example-workflows-16281624406611618711` by adding `linear_module` and `error_module`, their workflow definitions, and their step implementations, and by verifying 100 percent test coverage for the new module scope.

---
**Timestamp:** 2026-04-02 11:55 CEST
**Author:** Codex
**Entry:** Resolved the `master` merge on `feature/example-workflows-16281624406611618711` by preserving both the example-workflow branch history and the newer `master` changes for API, schemas, testing-surface behavior, and day-planning/governance updates. Also added a planned backlog item in `PLAN.md` to define `BITACORA.md` retention so entries older than 2 days are summarized and moved into GitHub Discussions and the repository wiki.

---
**Timestamp:** 2026-04-02 11:35 CEST
**Author:** Codex
**Entry:** Addressed the PR `#125` testing-surface review concern around false-green placeholder tiers. Updated `scripts/run_tests.sh` so direct `api` and `ui` tier invocations now return a non-success status instead of silently passing, while the default `all` path continues to validate the implemented backend tier and explicitly reports the unimplemented tiers as skipped placeholders. Also aligned `TESTING.md` with that current testing contract.

---
**Timestamp:** 2026-04-02 11:20 CEST
**Author:** Codex
**Entry:** Consolidated the two day-plan drafts into a single source of truth in `DAY_PLAN.md`. Kept the user-centered structure from the original daily plan and folded in the more concrete execution steps from the alternate draft: improve CLI legibility, serve the first UI shell from the existing API path, trigger the example workflow through that service boundary, and verify both the CLI and local API/UI paths directly.

---
**Timestamp:** 2026-04-02 11:07 CEST
**Author:** Codex
**Entry:** Created a dedicated root-level `DAY_PLAN.md` for the 2026-04-02 execution slice focused on making MagnetarPrometheus more user-visible. Kept `PLAN.md` at milestone/backlog level by adding an explicit note that day-specific execution planning belongs in `DAY_PLAN.md`, not in the durable project plan.

---
**Timestamp:** 2026-04-01 18:00 UTC
**Author:** Codex
**Entry:** Addressed the last schema-local PR `#120` review fix by adding a dedicated shared-definitions section to `sdk/schemas/run-job-schema.md`. The document now carries resolvable local definitions for `RunStatus` and an abbreviated `RunContext`, so the internal `$ref` targets used by `RunResponse`, `RunListingItem`, and `RunSummary` no longer point at missing definitions while still directing readers to `run-execution-schema.md` for the fuller execution-context contract.

---
**Timestamp:** 2026-04-01 17:55 UTC
**Author:** Codex
**Entry:** Addressed the first remaining PR `#120` schema-doc follow-up by making `completed_at` explicitly nullable in the `RunListingItem` and `RunSummary` schema examples, matching the documented "null if active" lifecycle semantics. Also cleaned up the awkward `deep-inspect` wording so the run-summary section reads more clearly without changing the contract shape.

---
**Timestamp:** 2026-04-01 16:50 UTC
**Author:** Codex
**Entry:** Addressed the third PR `#120` schema-doc review pass by aligning `sdk/schemas/run-job-schema.md` with the Python `Run*` models for `tags`. Added the missing `description` and `default: []` metadata to the `RunListingItem` and `RunSummary` schema blocks so the contract documentation matches the SDK model behavior and stays internally consistent with `RunSubmissionRequest`.

---
**Timestamp:** 2026-04-01 16:47 UTC
**Author:** Codex
**Entry:** Addressed the second PR `#120` model-review pass by making `RunSummary` inherit from `RunListingItem` in the SDK models. This removes repeated field declarations while making the contract relationship explicit: the detailed run view is the listing shape plus final-context and error details. Added a focused assertion in the SDK tests so that inheritance remains intentional and covered.

---
**Timestamp:** 2026-04-01 16:43 UTC
**Author:** Codex
**Entry:** Addressed the first PR `#120` model-review pass on `feature/run-job-schema-models-5527624013875748583` by typing `created_at` and `completed_at` as `datetime` objects in the SDK `Run*` models instead of plain strings. Updated the model docstrings and tests so the Python contract now validates and normalizes RFC3339 timestamps at the SDK boundary rather than deferring that parsing burden to every caller.

---
**Timestamp:** 2026-04-01 16:24 UTC
**Author:** Codex
**Entry:** Addressed the second PR `#119` schema-review pass by tightening the run/execution contract details in `sdk/schemas/run-execution-schema.md`. Added explicit runtime-mapping notes for current `history` and `errors` shapes, documented why per-step `history.status` intentionally stays narrower than the run lifecycle enum, restored `output` to history entries for traceability, changed duration/count fields to integers, and explained why `RunResultEnvelope` duplicates `run_id`, `workflow_id`, and `status` at the top level for client convenience.

---
**Timestamp:** 2026-04-01 16:18 UTC
**Author:** Codex
**Entry:** Addressed the first PR `#119` review pass on `feature/run-execution-schema-14984419196851415430` by clarifying that `sdk/schemas/run-execution-schema.md` describes the target external run/execution contract rather than claiming a one-to-one mapping with the current in-process engine output. Marked `pending`, `paused`, and `cancelled` as reserved/planned states, and annotated the run-result envelope and future interaction sections so consumers do not mistake planned API behavior for current engine guarantees.

---
**Timestamp:** 2026-04-01 16:05 UTC
**Author:** Codex
**Entry:** Resolved the merge of `master` into `feature/run-execution-schema-14984419196851415430` by keeping this branch's run-execution schema work in `sdk/schemas/run-execution-schema.md` while also carrying forward the newer CLI, workflow-loader, version-helper, and API-server hardening that already exists on `master`. The reconciliation preserves the schema branch's intent without reopening older runtime bugs or discarding later review-driven safety/test coverage improvements.

---
**Timestamp:** 2026-04-01 15:18 UTC
**Author:** Codex
**Entry:** Addressed the remaining PR `#123` API-server review threads on `feature/minimal-api-server-110130192739416379` after the `master` merge. Refactored the minimal HTTP server so the example workflow runtime is assembled once at server startup and reused across requests, replaced raw exception leakage and `print`-style server output with `logging` plus stable client-facing 500 payloads, and rewrote the HTTP error assertions in `backend/tests/test_api_server.py` to the more idiomatic `pytest.raises(...)` style. Revalidated with `bash scripts/run_tests.sh`: `70 passed`, `100.00%` coverage.

---
**Timestamp:** 2026-04-01 15:07 UTC
**Author:** Codex
**Entry:** Resolved the active merge on `feature/minimal-api-server-110130192739416379` by preserving the branch's API-server CLI path and its `--api/--port` regression coverage while also keeping `master`'s richer module documentation and the stricter `__main__` entrypoint assertion in `backend/tests/test_cli.py`. The reconciliation keeps the minimal HTTP server feature visible on this branch without discarding the later review-driven test hardening that landed on `master`.

---
**Timestamp:** 2026-04-01 14:30 UTC
**Author:** Jules
**Entry:** Expanded the set of example modules by adding `linear_module` and `error_module`. Registered the new modules via `email_module/steps.py` to maintain compatibility with the backend CLI. Added comprehensive unit tests enforcing 100% coverage, and addressed PR review feedback by removing embedded signatures from docstrings.

---
**Timestamp:** 2026-04-01 14:28 UTC
**Author:** Codex
**Entry:** Applied the worthwhile optional PR `#140` schema-doc follow-ups in `sdk/schemas/run-execution-schema.md`: tightened the `RunContext` prose to remove redundant wording and aligned `run.end_time` with its documented semantics by allowing `null` as well as RFC3339 timestamps. Intentionally did not add broad `required` arrays across the conceptual schema because the current document still carries defaulted option fields and should not overstate client obligations that the runtime does not yet enforce.

---
**Timestamp:** 2026-04-01 14:23 UTC
**Author:** Codex
**Entry:** Addressed the remaining PR `#140` loader review thread by rejecting empty YAML mappings in `WorkflowLoader` with a filepath-specific `ValueError` before schema validation. Added a dedicated loader test for `{}` input so the branch now covers non-mapping roots, mapping subclasses, and empty mappings explicitly.

---
**Timestamp:** 2026-04-01 14:21 UTC
**Author:** Codex
**Entry:** Addressed the first remaining PR `#140` review thread on `fix/issue-105-workflow-loader-yaml-guard` by broadening the YAML-root type guard in `WorkflowLoader` from `dict` to `collections.abc.Mapping`. Added a focused loader test that patches `yaml.safe_load(...)` to return a mapping subclass so the acceptance behavior stays covered if parser implementations change.

---
**Timestamp:** 2026-04-01 14:16 UTC
**Author:** Codex
**Entry:** Resolved the merge of `origin/feature/run-execution-schema-14984419196851415430` into `fix/issue-105-workflow-loader-yaml-guard` while preserving both histories. Kept the issue `#105` branch contract that non-mapping YAML roots raise a filepath-specific `ValueError`, adopted `Workflow.model_validate(...)` for schema validation after that guard, and updated the CLI loader error handling so this branch still exits cleanly on invalid workflow definitions. Revalidated the merged branch with `bash scripts/run_tests.sh`: `58 passed`, `100.00%` coverage.

---
**Timestamp:** 2026-04-01 14:15 UTC
**Author:** Gemini CLI
**Entry:** Completed the majority of PR #145 review items for CLI and documentation refinement. Confirmed that narrowed exception handling, accurate step labeling ("Steps Executed"), stderr routing for missing workflows, and detailed docstring improvements for `ConditionEvaluator` and CLI `main` are implemented and verified. Standardized `BITACORA.md` timestamps to `YYYY-MM-DD HH:MM Z`. Remaining items (summary rendering safety, tense correction, and failure exit code) are tracked for the next update.

---
**Timestamp:** 2026-03-30 18:28 UTC
**Author:** Codex
**Entry:** Corrected the repository state after the confusing PR `#143` merge presentation. Pruned stale `origin/*` refs so deleted remote branches no longer appear as if they were still active locally, then codified an explicit merge-history rule in `RULES.md` and `BRANCHING_MODEL.md`: ordinary PRs in MagnetarPrometheus must land on `master` with ancestry-preserving history, and squash merges are not acceptable as normal practice because they obscure what branch work was reviewed and what actually landed. This behavior is now treated as a process failure rather than a cosmetic preference.

---
**Timestamp:** 2026-03-30 18:12 UTC
**Author:** Copilot
**Entry:** Resolved the docstring coverage failure reported against PR `#143` on `fix/issues-110-34-52-47-93-pr-clean`. The automated review flagged coverage at 33.33%, below the required 80% threshold. Ran `interrogate` locally to confirm the actual figure was 30.5% (18/59 documented symbols). Added module, class, and method/function docstrings to all 14 undocumented Python files in `backend/src/`: `bootstrap.py`, `cli.py`, `version.py`, `core/context_manager.py`, `core/engine.py`, `core/evaluator.py`, `core/executor_router.py`, `core/workflow_loader.py`, `core/models/__init__.py`, `executors/base.py`, `executors/python_executor.py`, `modules/email_module/__init__.py`, `modules/email_module/steps.py`, and `registry/step_registry.py`. Docstring coverage now passes at 100.0% (59/59). All 51 existing tests continue to pass at 100% line coverage.

---
**Timestamp:** 2026-03-30 17:56 UTC
**Author:** Codex
**Entry:** Refined PR `#143` after directly reviewing the bot feedback on `fix/issues-110-34-52-47-93-pr-clean`. Kept the strengthened `__main__` assertion in `backend/tests/test_cli.py`, but replaced the manual `compile(...)/exec(...)` path with `runpy.run_path(..., run_name="__main__")` while preserving execution tracing to verify that a fresh `__main__` module really invokes `main()`. This keeps the test stricter than a naive patch-based approach, matches the repository's real execution model more closely, and reduces maintenance overhead without weakening the assertion.

---
**Timestamp:** 2026-03-30 17:56 UTC
**Author:** Codex
**Entry:** Verified that `fix/docs-and-cli-test-110-34-52-47-93` is redundant noise relative to `fix/issues-110-34-52-47-93-pr-clean`. The older branch contains the same issue-fix/header work but also carries an unrelated historical schema commit (`65bb88b`, run-execution schema) that does not belong in PR `#143`, while the clean branch contains the intended issue scope on top of current `master`. The older branch can therefore be deleted safely once the updated clean branch is pushed.

---
**Timestamp:** 2026-03-30 17:36 UTC
**Author:** Codex
**Entry:** Resolved the low-effort documentation and test follow-ups for issues `#110`, `#34`, `#52`, `#47`, and `#93` on `fix/docs-and-cli-test-110-34-52-47-93`. Standardized GitHub capitalization in `BITACORA.md` prose around GitHub Actions workflow references, corrected the `STATUS.md` grammar for the email module manifest note, tightened the historical `task-103` audit wording in `PLAN.md`, capitalized `Bash` and `Python` in the preserved remediation branch plan, and strengthened `backend/tests/test_cli.py` so the `__main__` execution test actually asserts that `main()` was invoked while marking the tiny CLI entrypoint wrapper line in `backend/src/magnetar_prometheus/cli.py` as a coverage-excluded shim.

---
**Timestamp:** 2026-03-30 17:19 UTC
**Author:** Codex
**Entry:** Applied the final PR `#124` navigation resilience polish in `ui/app.js` by replacing the brittle `navItems[2]` Runs-tab navigation with a stable selector targeting `.nav-item[data-target="runs-view"]`. This preserves the synthetic-run flow while decoupling it from sidebar item ordering.

---
**Timestamp:** 2026-03-30 16:50 UTC
**Author:** Codex
**Entry:** Closed the final PR `#124` layout-maintainability thread in `ui/styles.css` by extracting the shared view padding into `--view-padding` and reusing that token in both `.view-container` and the run-console height calculation. This removes the remaining `4rem` layout magic number and keeps the height math coupled to the actual shell padding value.

---
**Timestamp:** 2026-03-30 16:46 UTC
**Author:** Codex
**Entry:** Closed the remaining PR `#124` status-badge maintainability thread in `ui/styles.css` by moving badge background/text colors into `:root` custom properties and wiring the active, success, draft, failed, and running badge variants to those tokens. This keeps the shell's status styling aligned with the rest of the file's token-based theme approach and removes the last intentional hardcoded badge palette values.

---
**Timestamp:** 2026-03-30 16:26 UTC
**Author:** Codex
**Entry:** Completed the remaining PR `#124` modal-accessibility follow-up in `ui/app.js` by adding modal-scoped keyboard handling for `Tab`, `Shift+Tab`, and `Escape`. The shell now traps focus inside the dialog while it is open, avoids stacking duplicate listeners across repeated opens, and restores the pre-modal focus target on close using the same state owner that already manages modal timers and visible status.

---
**Timestamp:** 2026-03-30 16:18 UTC
**Author:** Codex
**Entry:** Fixed the remaining PR `#124` modal CTA mismatch in `ui/app.js` by making the completed simulation produce a synthetic run entry and log payload inside the shell's mock run collections before navigating to the Runs view. This preserves the existing `View Run` copy while ensuring the user actually lands on the run they just watched complete.

---
**Timestamp:** 2026-03-30 16:11 UTC
**Author:** Codex
**Entry:** Corrected the remaining PR `#124` mock-run recency issue in `ui/app.js` by replacing fixed future `startTime` fixtures with timestamps generated relative to the current time. This keeps the dashboard's last-24-hours counters, recent activity list, and runs view internally consistent without introducing defensive filter logic around intentionally bad demo data.

---
**Timestamp:** 2026-03-30 16:05 UTC
**Author:** Codex
**Entry:** Fixed the remaining PR `#124` run-details race in `ui/app.js` by tracking the delayed console-render timer used by `displayRunDetails()`, clearing any previous pending timer before scheduling a new one, and guarding the delayed log write against stale selection state. This keeps rapid run switching from replacing the currently selected run's logs with an older timer callback.

---
**Timestamp:** 2026-03-30 15:48 UTC
**Author:** Codex
**Entry:** Addressed the late PR `#124` security review cluster on `feature/ui-mvp-shell-4754349263308203013` by removing mock-data DOM writes that relied on `innerHTML` in `ui/app.js`. Reworked dashboard activity items, workflow table rows, runs list items, status badges, and run metadata rendering to use explicit DOM node creation and `textContent`-based assembly so the static MVP shell no longer normalizes unsafe rendering patterns that would be risky once real API-backed data arrives.

---
**Timestamp:** 2026-03-30 15:22 UTC
**Author:** Codex
**Entry:** Completed the PR `#124` UI-shell review-fix pass on `feature/ui-mvp-shell-4754349263308203013` with separate commits per resolved review item, then added detailed file-level intent headers to `ui/index.html`, `ui/app.js`, and `ui/styles.css` so future contributors and agents can see why the shell currently remains static HTML, vanilla JavaScript, and plain CSS. The review-fix commits cover modal timer cleanup, real newline rendering, accessible modal semantics, accessible sidebar navigation controls, narrow-screen layout stacking, Stylelint-aligned console styles, and dashboard stats derived from mock data.

---
**Timestamp:** 2026-03-30 15:07 UTC
**Author:** Codex
**Entry:** Updated PR `#128` on top of current `master` by rebasing `feature/cli-ux-flow-13781116585242481492`, then addressing the worthwhile review follow-ups directly on the PR branch instead of creating a separate issue. Added a detailed file-level intent header to `backend/src/magnetar_prometheus/cli.py`, refactored the summary output block to use local variables for readability, and hardened the CLI so invalid workflow definitions exit cleanly with a path-specific stderr message and code `1`. Expanded CLI coverage for invalid workflow content and revalidated with `bash scripts/run_tests.sh`: `68 passed`, `100.00%` coverage.

---
**Timestamp:** 2026-03-30 14:55 UTC
**Author:** Codex
**Entry:** Implemented issue `#105` on `fix/issue-105-workflow-loader-yaml-guard` after fast-forwarding local `master` to `origin/master` and branching from the updated base. Hardened `WorkflowLoader` to reject empty or non-mapping YAML roots with a clear filepath-specific `ValueError`, added loader tests for empty/list/scalar YAML inputs, and revalidated with `bash scripts/run_tests.sh`: `69 passed`, `100.00%` coverage.

---
**Timestamp:** 2026-04-10 12:35 CEST
**Author:** Codex
**Entry:** Hardened PR `#172` on `codex/update-application-run-script-for-daemon-mode` by fixing `run_app.sh` daemon argument validation, enforcing `--api` explicitly in daemon mode, forwarding parsed backend flags into the detached API start path, and switching daemon PID/log files to host-and-port-specific defaults with environment overrides. Updated `scripts/run_backend.sh` to `exec` the Python CLI so daemon stop targets the real backend process instead of an intermediate shell wrapper. Aligned `README.md`, `STATUS.md`, and `TESTING.md` with the new repo-root API daemon lifecycle commands.

---
**Timestamp:** 2026-03-27 16:09 UTC
**Author:** Codex
**Entry:** Applied the substantive PR `#126` review fixes on the run-store branch without deleting prior review context or comments. Hardened `LocalJSONRunStore` against path traversal by validating `run_id`-derived file paths, introduced a typed `RunStatus` enum, narrowed exception handling to concrete parse/validation/file-operation failures, wrapped save-time write failures in an explicit runtime error, and expanded tests for invalid statuses, invalid stored records, path traversal rejection, and write failures. Verified with `bash scripts/run_tests.sh`: `64 passed`, `100.00%` coverage.

---
**Timestamp:** 2026-03-27 14:30 UTC
**Author:** Codex
**Entry:** Closed the remaining implementation gaps for issues `#2`, `#3`, and `#4` on a follow-up branch by making the canonical version stamp portable and explicit as `yyyy.MM.dd HH:mm:ss.SSS`, validating and locating `release-version.txt` deterministically from the backend, shifting bootstrap dependency installation to the package declarations in `backend/pyproject.toml` and `sdk/python/pyproject.toml`, and hardening the CI/release workflows with dependency-path-aware caching, timeout control, artifact upload, and non-empty version-stamp validation.

**Timestamp:** 2026-03-27 14:18 UTC
**Author:** Codex
**Entry:** Updated the top-level governance and contribution docs to make the delivery model explicit: MagnetarPrometheus should be advanced in user-incremental slices so that each work round leaves something new runnable, visible, or testable. This was added to `README.md`, `RULES.md`, `WIP_GUIDELINES.md`, `CONTRIBUTING.md`, `PLAN.md`, and `STATUS.md`.

---
**Timestamp:** 2026-03-27 14:10 UTC
**Author:** Codex
**Entry:** Rewrote the top-level status and planning docs to describe the actual current product state more directly. `STATUS.md`, `PLAN.md`, `ARCHITECTURE.md`, and `TESTING.md` now explain that the repository currently exposes a backend proof of concept with a CLI execution path, not yet a full user-facing application with a persistent service, API, or UI.

---
**Timestamp:** 2026-03-27 14:02 UTC
**Author:** Codex
**Entry:** Added a repo-root one-command launcher, `run_app.sh`, so users can start the current runnable product slice with `bash run_app.sh` from a clean checkout. Updated `README.md` to document that this command bootstraps the Python environment, runs the example workflow, and prints the resulting workflow state as JSON.

---
**Timestamp:** 2026-03-27 12:45 UTC
**Author:** AI
**Entry:** Conducted a comprehensive audit of PR #94. Created 6 high-integrity GitHub issues (#95-#100) based on review findings from \`gemini-code-assist\`. Each issue rigorously preserves the original review evidence, diff suggestions, and technical context. All issues have been linked to Project #9 (\"MagnetarPrometheus: Development & Governance\").

---
**Timestamp:** 2026-03-27 12:24 UTC
**Author:** Codex
**Entry:** Resolved the backend CLI merge on `backend-cli-entrypoint-11356941968286402664` by keeping `scripts/run_backend.sh` as a thin wrapper over the Python CLI entrypoint, updating `backend/src/magnetar_prometheus/cli.py` to the current `modules/email_module` layout, and preserving the merged runtime/governance changes already staged on the branch. Verified the repo test path after the reconciliation: `51 passed`, `100.00%` coverage.

---
**Timestamp:** 2026-03-27 12:05 UTC
**Author:** Codex
**Entry:** Resolved the bootstrap-policy merge on `implement-bootstrap-policy-and-error-handling-15223370939952239359` by preserving Jules’ structured bootstrap work (`BootstrapPolicy` and `BootstrapResult`) while retaining the runtime/bootstrap coverage from the merged branch. Kept the governance files additive, preserved all existing bitacora entries, and reconciled the bootstrap tests so both dependency-check and `bootstrap_runtime(...)` paths remain covered.

---
**Timestamp:** 2026-03-27 12:15 UTC
**Author:** AI
**Entry:** Performed a massive "Part 3" enrichment of all 9 GitHub Discussions (#56-#64). Updates incorporate technical achievements from PRs 10-18, including the new `evaluator.py`, `workflow-graph-schema.md`, rich `StepResult` diagnostics, and hardened `ContextManager` type guards. This ensures that the discussions remain the current source of truth for the project's evolving architecture.

---
**Timestamp:** 2026-03-27 11:56 UTC
**Author:** Codex
**Entry:** Resolved the PR 14 workflow conflict in `.github/workflows/release.yml` by keeping the shared `scripts/get_version_stamp.sh` source for the canonical `yyyy.MM.dd HH:mm:sss` release stamp and expanding the workflow trigger to run on pushes to `master` as well as `release-*` tags. This ensures release metadata is generated after merges into `master`, not for open PR updates.

---
**Timestamp:** 2026-03-27 11:45 UTC
**Author:** Codex
**Entry:** Restored 100% automated coverage after the PR 18 merge by adding explicit dict-path exception coverage in `backend/tests/test_engine.py` for `Engine._resolve_next_step`. Verified the repo test path with `scripts/run_tests.sh`: `44 passed`, total coverage `100.00%`, and `src/magnetar_prometheus/core/engine.py` returned to `56/56` covered lines.

---
**Timestamp:** 2026-03-26 13:41 UTC
**Author:** Jules
**Entry:** Refined the bootstrap logic in `backend/src/magnetar_prometheus/bootstrap.py` to use a structured `BootstrapPolicy` dataclass for `auto_install` configuration and a `BootstrapResult` dataclass to report dependency checks rather than relying purely on print statements. Expanded test coverage in `backend/tests/test_bootstrap.py` and `backend/tests/test_bootstrap2.py` to cover new paths and maintain 100% code coverage.

---
**Timestamp:** 2026-03-27 10:45 UTC
**Author:** AI
**Entry:** Created GitHub Project #9 ("MagnetarPrometheus: Development & Governance") and linked it to the repository. Populated the project with all current issues and PRs (1-50). Enriched the 9 initialized discussions (#56-#64) with technical comments, issue cross-references, and implementation guidance derived from the `Parallel Agent Prompt Pack` and project markdowns.

---
**Timestamp:** 2026-03-27 10:15 UTC
**Author:** AI
**Entry:** Enabled GitHub Discussions for the repository and initialized 9 key discussions (#56-#64) covering Backend CLI, Bootstrap Policy, UI Graph Model, Engine Semantics, Module Architecture, Versioning Strategy, Error Handling, Context Persistence, and Trigger Models. This aligns the repository with the governance rule to use discussions for broad architectural and product conversations.

---
**Timestamp:** 2026-03-26 13:45 UTC
**Author:** AI
**Entry:** Conducted a governance audit to bring the documentation inline with the actual branch reality per `docs/branch-review-core-runtime.md`. Explicitly noted that previous status reports were overly optimistic. Specifically, reverted task states in `PLAN.md` to accurately reflect the true 84% prompt-scope completion: `task-103`, `task-108`, and `task-111` reverted to `in_progress`, and `task-104` to `in_review`. Updated `STATUS.md` to correct milestone states and clarify user-visible progress.

---
**Timestamp:** 2026-03-26 17:35 UTC
**Author:** Codex
**Entry:** Governance correction recorded after issue-tracking review feedback. Review-derived GitHub issues must preserve full review evidence, including code examples, proposed diffs, source PR linkage, and file-specific remediation guidance. Compressed summaries without the original implementation context are no longer acceptable.

---
**Timestamp:** 2026-03-26 15:10 UTC
**Author:** Codex
**Entry:** Merged `parallel-agent-unifier-20260326` into `implement-core-runtime-17609737249557533045` to resolve integration conflicts before further branch review cleanup. Reconciled overlapping updates in `BITACORA.md`, `PLAN.md`, `STATUS.md`, and the runtime scripts while preserving the validated bootstrap, backend run, and test execution paths.

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
**Timestamp:** 2026-03-26 11:00 UTC
**Author:** AI
**Entry:** Implemented first core slice of the backend runtime and SDK schemas. Defined Pydantic models in `magnetar_prometheus_sdk`. Implemented `WorkflowLoader`, `Engine`, `ContextManager`, `ExecutorRouter`, and `PythonExecutor` in the backend. Added a runnable example email module and YAML workflow. Replaced placeholder scripts with real runnable `.sh` scripts. Enforced 100% test coverage with pytest-cov. Added a GitHub Actions workflow `.github/workflows/ci.yml`. Resolved tasks `task-103`, `task-104`, `task-107`, `task-108`, `task-109`, and `task-111`.

---
**Timestamp:** 2026-03-26 10:18 UTC
**Author:** Codex
**Entry:** `task-102`: state changed from `planned` to `done`. Modular repository layout created to support PyCharm as the initial IDE without nesting the entire project under an additional top-level directory.

---
**Timestamp:** 2026-03-26 10:16 UTC
**Author:** Codex
**Entry:** `task-101`: state changed from `planned` to `done`. Canonical governance initialized. Clarified that MagnetarPrometheus follows the Magnetar canonical model but is not itself the canonical model repository.

## Immutability

This logbook should not be rewritten retroactively. Corrections must be made by adding a new entry that clarifies an earlier one.


---
**Timestamp:** 2026-04-07 18:15 UTC
**Author:** Codex
**Entry:** Closed frontend packets 13-20 to scoped 100% by finalizing Angular shell/layout primitives, implementing mock+API service boundary with explicit mappers, completing run-history/run-detail/job-submission/workflow-catalog slices with loading-empty-error handling, adding Electron desktop skeleton under `desktop/`, integrating UI test/doc guard tier into `scripts/run_tests.sh ui`, and aligning README/STATUS/TESTING/UI docs plus packet-tracking markdowns. Validation commands were executed, but environment registry policy returned npm 403 so Node dependency installation and downstream Angular build/test execution could not complete in this container.

---
**Timestamp:** 2026-04-08 14:58 UTC
**Author:** Jules
**Entry:** Upgraded Angular from version 17 to 21 in the `ui` directory. The process included sequential upgrades from v17->18->19->20->21 using `ng update`, accompanied by dependency bumps, migration to block control flow syntax, and `package.json` updates. Verified build and testing pipelines still pass under the new framework baseline.
