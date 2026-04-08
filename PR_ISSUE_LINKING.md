# PR Issue Linking

Use explicit issue references in every pull request body.

## Rules

- Use `Fixes #<id>` or `Closes #<id>` only when merging that PR should automatically close the issue.
- Use `Related to #<id>` when the PR is partial, foundational, stacked, or only provides context for the issue.
- Do not link unrelated issues just because they are in the same broad area.
- Prefer a dedicated `## Related Issues` section near the top of the PR body.
- For stacked PRs, link the same issue in each PR, but describe the role precisely:
  - foundation
  - first increment
  - completion
  - follow-up

## Recommended PR Body Pattern

```md
## Related Issues
- Fixes #123
- Related to #124 because this PR only delivers the frontend half.
- Related to #125 as the validation/tooling follow-up.
```

## When To Use `Fixes`

Use `Fixes #<id>` only if:

- the issue's acceptance criteria are fully satisfied by the PR
- no major remaining scope is intentionally deferred
- you want GitHub to auto-close the issue when the PR merges

## When To Use `Related to`

Use `Related to #<id>` if:

- the PR is one slice of a larger issue
- the issue remains open after merge
- the PR is enabling work for a later issue
- the PR is part of a stacked branch sequence

## UI Stack Example

- PR `#161`: `Related to #155` as workspace foundation
- PR `#162`: `Related to #155`, `Related to #154`
- PR `#163`: `Related to #155`, `Related to #154`
- PR `#164`: `Related to #155`
- PR `#165`: `Related to #155`

## Avoid

- linking backend runtime issues from frontend-only PRs unless the PR directly changes that runtime scope
- using `Fixes` for issues that still have remaining API, CI, or follow-up work
- relying only on issue comments when the PR body itself should carry the traceability
