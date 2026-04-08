# Feature Branch Plan: Upgrade Angular to 21

## Branch

`feature/upgrade-angular-21`

## Problem

The UI application in `ui/` is still pinned to Angular 17.3.x. The goal of this branch is to prepare and execute the upgrade to Angular 21 while preserving the current mock/API transport modes, validation scripts, and documentation guardrails.

## Approach

1. Audit the current UI project files that are sensitive to Angular version changes.
2. Upgrade the Angular packages and align the supporting toolchain versions required by Angular 21.
3. Adjust any config or script changes needed for the new framework baseline.
4. Run the existing UI validation commands and fix regressions.
5. Confirm the branch is still aligned with the repository’s documentation and validation expectations.

## Plan of Work

- Inspect `ui/package.json`, `ui/package-lock.json`, and Angular config files for upgrade-sensitive entries.
- Identify any TypeScript, RxJS, zone.js, or builder version constraints introduced by Angular 21.
- Apply targeted package/config updates only where needed.
- Validate build, test, and docs-check flows after the upgrade.
- Capture any follow-up issues that remain after the framework bump.

## Status Updates
- Executed `ng update` from Angular 17 -> 18 -> 19 -> 20 -> 21.
- Ensured migration to Angular 21 compatible syntax and configuration blocks was successfully applied to existing component models.
- Re-installed dependancies and verified all core building checks via `npm run build`, `npm run test:ci`, and `npm run check:docs`.
- Verified changes passed properly.
- Refreshed `ui/package-lock.json` after the Angular 21 dependency bump so `npm ci` works again on the upgraded branch.
- Addressed the first PR `#165` review follow-up by replacing object-reference `@for` tracking with stable identifiers and simplifying repeated conditional template blocks with `@else if` / `@else`.

## Notes

- Keep the current UI behavior stable unless Angular 21 forces a change.
- Prefer small, reversible edits over a broad rewrite.
- Treat validation failures as part of the upgrade work, not as a separate cleanup step.
