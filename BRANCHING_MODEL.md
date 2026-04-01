# Branching Model for MagnetarPrometheus

<!--
Why this file exists in this form:

- This file is the compact branch-lifecycle contract for the repository. It complements
  `RULES.md` by stating the Git model in the narrowest possible form so a contributor can
  understand branch expectations quickly without scanning the entire governance set.
- The document stays short on purpose. Its job is not to duplicate every rule, but to make
  the allowed branch types and merge expectations unmistakable at the point where branch
  work is created and reviewed.
- Merge semantics are included here because branch names alone are not enough to preserve a
  readable project history. How a branch lands on `master` determines whether later readers
  can connect reviewed work, issue closure, and the final repository state without guesswork.
- The repository treats history readability as an implementation concern, not cosmetic
  polish. A branch that "contains the right code" but lands in a way that obscures what was
  reviewed is still a process failure.
- This file should therefore make bad merge behavior impossible to misread as acceptable.
  In particular, ancestry-breaking merges for ordinary PRs are not a stylistic preference;
  they are a workflow violation unless explicitly documented as an exception.
-->

MagnetarPrometheus uses a lightweight GitFlow-style model.

## Branch Types

- `master`: stable release line
- `develop`: optional integration branch
- `feature/*`: new capabilities
- `fix/*`: non-emergency fixes
- `chore/*`: maintenance work
- `experiment/*`: exploratory work
- `hotfix/*`: urgent production or release-line fixes

## Rules

- Branch names follow `<type>/<short-description>`.
- Feature and fix branches should be rebased before merge.
- Standard PRs must be merged in a way that preserves branch ancestry on `master`.
- Squash merges are not the default or acceptable normal path for repository work because
  they hide which reviewed branch commits actually landed.
- Pull requests should reference task IDs and documentation updates.
- Documentation-sensitive changes must update the canonical governance files when applicable.
