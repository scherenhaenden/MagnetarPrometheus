# Contributing to MagnetarPrometheus

## Development Setup

Open the repository root in your IDE. For Python work, treat `backend/` as the Python subproject and use its `pyproject.toml`.

## Contribution Process

1. Review [PLAN.md](/home/edward/Development/MagnetarPrometheus/PLAN.md) and [STATUS.md](/home/edward/Development/MagnetarPrometheus/STATUS.md).
2. Choose or confirm a task in an allowed working state.
3. Create a branch following [BRANCHING_MODEL.md](/home/edward/Development/MagnetarPrometheus/BRANCHING_MODEL.md).
4. Make changes with matching documentation updates where needed.
5. Record decisions and state changes in [BITACORA.md](/home/edward/Development/MagnetarPrometheus/BITACORA.md).
6. Move the task to `in_review` before opening a pull request.
7. If GitHub project operations are active, create or link a GitHub issue for the work and use a GitHub discussion for larger product or architecture questions.
8. If an issue is created from a code review, preserve the review evidence in the issue body, including concrete code examples, proposed diffs, and exact file references when available.
9. Prefer increments that give the user something new to run, inspect, or validate by the end of the round.
10. Parallel work must be divided by disjoint write ownership so contributors do not collide in the same surface.

## Pull Request Expectations

- reference task IDs
- summarize behavioral changes
- note testing performed
- include documentation updates when scope or governance changed
- mention user-visible impact, not only technical implementation details
- state clearly whether a change is user-visible or internal-only; explain what a user can try after the change
- "done" does not imply a finished product experience if only an internal slice is complete
- if follow-up issues are created from review comments, keep the full implementation context in those issues instead of replacing it with a short paraphrase
