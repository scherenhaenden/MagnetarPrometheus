# Rules of MagnetarPrometheus

<!--
Why this file exists in this form:

- This file is the repository's hard governance layer. It is intentionally stricter than
  README-style guidance because it defines what contributors, agents, and automation are
  allowed to treat as normal operating procedure.
- The rules here are phrased as repository-level constraints rather than personal advice.
  That distinction matters because this document is meant to survive changes in tools,
  agents, and maintainers without losing the expected operating model.
- Branching, planning, status tracking, and documentation rules live together here on
  purpose. MagnetarPrometheus relies on those artifacts as part of the product-delivery
  process, so governance is not separate from implementation quality.
- Merge behavior belongs here because repository history is part of the system's audit
  surface. If merges destroy ancestry, hide reviewed branch work, or leave ambiguous
  branch state behind, they create operational confusion even when the resulting code is
  technically present on `master`.
- This file should bias toward explicitness over convenience. A contributor should be able
  to read it and understand not just what is preferred, but what is considered a process
  failure that must not be normalized.
- If a workflow exception is ever necessary, the exception must be documented in
  `BITACORA.md` rather than silently replacing the normal rule with ad hoc behavior.
-->

These rules codify how MagnetarPrometheus operates under the Magnetar Canonical Project Model. The repository must comply unless a formal exception is documented in [BITACORA.md](/home/edward/Development/MagnetarPrometheus/BITACORA.md).

## Naming Conventions

- Repositories: `magnetar-<domain>-<descriptor>`
- Branches: `<type>/<short-description>` where `type` is `feature`, `fix`, `chore`, `experiment`, or `hotfix`
- Tasks and blockers: `kebab-case`
- YAML keys: `lower_snake_case`
- Canonical governance file names must remain stable across Magnetar repositories

## Required Files

The following files must exist unless an exemption is logged in [BITACORA.md](/home/edward/Development/MagnetarPrometheus/BITACORA.md):

- `README.md`
- `PLAN.md`
- `BITACORA.md`
- `REQUIREMENTS.md`
- `ARCHITECTURE.md`
- `RULES.md`
- `STATUS.md`
- `TESTING.md`
- `BLOCKERS.md`
- `BRANCHING_MODEL.md`
- `WIP_GUIDELINES.md`
- `CONTRIBUTING.md`
- `projects/<project>.project.yml` or an instantiated equivalent derived from the template

## Versioning Standard

- Canonical version and release stamps use the format `yyyy.MM.dd HH:mm:sss`
- The same timestamp-oriented format should be reused across release notes, pipeline artifacts, and other operational metadata where practical

## Branching Conventions

- `master` is the release line and should only receive documented, validated merges.
- `develop` is optional and may aggregate completed work before stabilization.
- `feature/*` branches may start from `master` or `develop` and should be rebased before merge.
- `hotfix/*` branches start from `master` and require a follow-up update in [STATUS.md](/home/edward/Development/MagnetarPrometheus/STATUS.md).
- Every pull request must reference impacted tasks and corresponding [BITACORA.md](/home/edward/Development/MagnetarPrometheus/BITACORA.md) entries.
- Normal pull requests must be merged with ancestry-preserving history. Squash merges are
  not acceptable for standard feature/fix/chore PRs because they sever the visible link
  between reviewed branch work and the resulting `master` history.
- If a squash merge is ever used as an explicit exception, that exception and its reason
  must be documented in [BITACORA.md](/home/edward/Development/MagnetarPrometheus/BITACORA.md)
  before the history is considered clean again.

## Allowed Task States

1. `planned`
2. `ready`
3. `in_progress`
4. `in_review`
5. `blocked`
6. `done`

Allowed progression is normally:

- `planned` to `ready`
- `ready` to `in_progress`
- `in_progress` to `in_review`
- `in_review` to `done` (Note: "done" means the specific task slice is complete; it must not be used to imply a finished product experience when only an internal slice is complete)
- any active state to `blocked` when a tracked blocker is present

## Work-In-Progress Constraints

- Default WIP limit per individual or AI agent: 2 tasks in `in_progress`
- Exceeding the limit requires explicit approval recorded in [WIP_GUIDELINES.md](/home/edward/Development/MagnetarPrometheus/WIP_GUIDELINES.md) and [BITACORA.md](/home/edward/Development/MagnetarPrometheus/BITACORA.md)
- Work should be organized around user-incremental delivery. A reasonable default expectation is that each work round leaves a newly testable, runnable, or inspectable increment for the user or operator.
- Parallel work must be divided by disjoint write ownership so contributors do not collide in the same surface.

## Blocker Lifecycle

1. Discovery: create an entry in [BLOCKERS.md](/home/edward/Development/MagnetarPrometheus/BLOCKERS.md) with ID, description, severity, owner, and timestamp.
2. Assessment: reflect the risk in [STATUS.md](/home/edward/Development/MagnetarPrometheus/STATUS.md) and add mitigation notes to [BITACORA.md](/home/edward/Development/MagnetarPrometheus/BITACORA.md).
3. Escalation: escalate if unresolved within one business day unless explicitly waived.
4. Resolution: log the solution in [BITACORA.md](/home/edward/Development/MagnetarPrometheus/BITACORA.md) and mark the blocker resolved.
5. Retrospective: capture lessons learned in the relevant project documentation.

## Documentation Discipline

- [BITACORA.md](/home/edward/Development/MagnetarPrometheus/BITACORA.md) records state changes, decisions, and exceptions chronologically.
- [STATUS.md](/home/edward/Development/MagnetarPrometheus/STATUS.md) is updated at least daily during active work or after each merge.
- [PLAN.md](/home/edward/Development/MagnetarPrometheus/PLAN.md) is the planning source of truth for milestones and task assignments.
- Daily updates must include user-visible progress, not just technical deltas.
- Status, plan, and architecture documents, as well as pull requests, must state clearly whether the latest increment is actually user-testable or still only an internal capability.
- Actionable work should be mirrored in GitHub issues whenever the repository is using GitHub operationally.
- Open design, product, and governance questions should be tracked in GitHub discussions when they are broader than a single task.
- GitHub issues created from reviews must preserve the original review evidence instead of compressing it into a short summary.
- When a review contains concrete code examples, proposed diffs, quoted review prompts, or file-specific remediation guidance, that material must be copied into the issue body or linked verbatim enough to preserve the implementation context.
- Rewriting an issue for clarity is allowed, but the rewrite must retain the original code relation, examples, source PR/review linkage, and enough detail that a later contributor can act without reopening the original review thread.
- If part of a review finding is stale or already resolved, mark that status explicitly, but do not delete the historical implementation guidance from the issue body.

## AI Agent Responsibilities

- Parse the project YAML before acting on planning-sensitive tasks.
- Do not prepare a PR state without the task first reaching `in_review`.
- Document assumptions and deviations in [BITACORA.md](/home/edward/Development/MagnetarPrometheus/BITACORA.md).
- When using GitHub, keep task execution aligned with issues and use discussions for unresolved design questions.
- Do not compress review-derived GitHub issues into abstract summaries that drop code examples or remediation details.
- Prefer slices that expose one more user-testable increment per round trip instead of accumulating only invisible internal work across many turns.

## Compliance And Enforcement

- CI should validate the presence and basic structure of required files.
- Periodic audits should verify planning, status, branching, and blocker compliance.
- CI and release pipelines should enforce the active versioning and testing rules.
