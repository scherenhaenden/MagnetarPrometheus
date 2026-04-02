# Branching Model for MagnetarPrometheus

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
- Pull requests should reference task IDs and documentation updates.
- Documentation-sensitive changes must update the canonical governance files when applicable.
