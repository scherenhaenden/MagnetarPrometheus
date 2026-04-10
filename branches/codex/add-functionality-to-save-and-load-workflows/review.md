# PR 176 Review

## Scope Reviewed

- `ui/src/app/features/workflow-studio/workflow-studio-page.component.ts`
- `ui/src/app/features/workflow-studio/workflow-studio-page.component.html`
- `ui/src/app/features/workflow-studio/workflow-studio-page.component.css`
- `ui/src/app/features/workflow-studio/workflow-studio-page.component.spec.ts`

## Fixed In This Pass

1. Corrupt local-storage entries no longer crash project restore.
   - `restoreProjects()` now rejects `null` and non-object entries before reading `entry.nodes`.
   - Added a spec that seeds `[null, validProject]` and proves only the valid project is restored.

2. Project IDs now use UUIDs instead of timestamp-only identifiers.
   - `createProjectId()` now prefers `crypto.randomUUID()`.
   - A narrow fallback remains for environments where `randomUUID()` is unavailable.
   - Added a spec that proves the UUID path is used when available.

## Already Covered Before This Pass

1. Stale execution state when creating/loading projects.
   - `newProject()` and `loadProject()` already call `stopWorkflow()`.
   - That clears `isRunning`, `activeNodeId`, `completedNodeIds`, and pending timers.

## Still Open After This Pass

1. Save-order UX for updated projects.
   - Updating an existing project still replaces it in place instead of moving it to the top of `savedProjects`.
   - Review ask: recently updated projects should be easiest to find in the selector.

2. Storage access hardening.
   - The component now uses optional access to `globalThis.localStorage`, which avoids a direct reference failure.
   - It still does not wrap storage reads/writes in `try/catch` for browser privacy restrictions, quota failures, or denied storage access.
   - Review ask: guard both restore and persist against unavailable or failing storage.

## Current Assessment

- TypeScript app compile: passes
- TypeScript spec compile: passes
- Review items 3 and 4 from the earlier audit are now addressed.
- PR `#176` is closer, but not fully review-clean yet because the two items above still remain.
