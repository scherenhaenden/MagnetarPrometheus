# Agent 11 Prompt Index: Independent Frontend Work Packets

## Execution Progress Snapshot (2026-04-07)

- Packet 11 (index/orchestration): **100%** complete.
- Packet 12 (workspace skeleton): **100%** complete.
- Packet 13 (web shell): **85%** complete (routed shell + placeholders implemented).
- Packet 14 (data contract boundary): **80%** complete (contracts + mock service implemented; HTTP adapter pending).
- Packet 15 (design/layout primitives): **70%** complete (reusable shell frame exists, token system still minimal).
- Packet 16 (run history slice): **75%** complete (history/detail UI in mock mode).
- Packet 17 (job submission slice): **75%** complete (form + validation + mock submission wired).
- Packet 18 (desktop shell skeleton): **0%** complete (not started in this branch).
- Packet 19 (frontend testing/doc guards): **35%** complete (basic Angular spec path retained; guard tooling pending).
- Packet 20 (local run flow): **80%** complete (UI README/run steps expanded; root script integration pending).

**Overall packet-stream progress (11→20): ~60%.**


## Purpose

This index exists so frontend/application scaffolding work can be delegated in
parallel without collapsing into one oversized prompt.

Every linked file below is intentionally scoped so it can be handed to Gemini
or another coding agent as an independent packet with minimal collision risk.

## Read First Rule

Every prompt in this set begins from the same requirement:

- Read the rules in the markdowns in the root of the project first.
- Follow those rules strictly.
- Keep comments and docstrings extremely explicit and intentionally long.
- Use Angular for the web surface.
- Do not use React.

## Prompt Set

- [12-frontend-workspace-skeleton.md](/home/edward/Development/MagnetarPrometheus/work-/for-agents/12-frontend-workspace-skeleton.md)
  - Angular workspace and directory foundation only.
- [13-frontend-web-shell.md](/home/edward/Development/MagnetarPrometheus/work-/for-agents/13-frontend-web-shell.md)
  - First browser-visible application shell only.
- [14-frontend-data-contract-boundary.md](/home/edward/Development/MagnetarPrometheus/work-/for-agents/14-frontend-data-contract-boundary.md)
  - Frontend-side models, API facades, and mock adapters only.
- [15-frontend-design-system-and-layout.md](/home/edward/Development/MagnetarPrometheus/work-/for-agents/15-frontend-design-system-and-layout.md)
  - Design tokens, layout primitives, and reusable shell UI only.
- [16-frontend-run-history-slice.md](/home/edward/Development/MagnetarPrometheus/work-/for-agents/16-frontend-run-history-slice.md)
  - Run-history and run-detail placeholder/product slice only.
- [17-frontend-job-submission-slice.md](/home/edward/Development/MagnetarPrometheus/work-/for-agents/17-frontend-job-submission-slice.md)
  - Job-submission screen and form boundary only.
- [18-desktop-shell-skeleton.md](/home/edward/Development/MagnetarPrometheus/work-/for-agents/18-desktop-shell-skeleton.md)
  - Desktop host shell only.
- [19-frontend-testing-and-doc-guards.md](/home/edward/Development/MagnetarPrometheus/work-/for-agents/19-frontend-testing-and-doc-guards.md)
  - Testing, linting, and documentation-presence guardrails only.
- [20-frontend-local-run-flow.md](/home/edward/Development/MagnetarPrometheus/work-/for-agents/20-frontend-local-run-flow.md)
  - Run scripts, README updates, and local developer flow only.

## Recommended Parallelization

These can be run independently if write ownership is respected:

- `12` can run independently from `18` and `19`.
- `14` can run independently from `15`.
- `16` can run independently from `17` if each stays in its own feature area.
- `18` should not rewrite Angular app internals.
- `19` should not redesign product features.
- `20` should focus only on local developer/run path docs and scripts.

## Important Rule

Do not ask one agent to do all of them at once. These prompts are split so the
work can be parallelized and reviewed as small, comprehensible slices.
