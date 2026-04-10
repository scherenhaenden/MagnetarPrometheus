#!/bin/bash
set -euo pipefail

# Helper to check if a comment already exists in a discussion
comment_exists() {
  local discussion_id="$1"
  local marker="$2"
  gh api graphql -F id="$discussion_id" -f query='
    query($id: ID!) {
      node(id: $id) {
        ... on Discussion {
          comments(first: 100) {
            nodes {
              body
            }
          }
        }
      }
    }' --jq ".data.node.comments.nodes[].body | contains(\"$marker\")" | grep "true" > /dev/null
}

# Helper to post a comment with validation
post_comment() {
  local discussion_id="$1"
  local body="$2"
  local marker="$3"

  if comment_exists "$discussion_id" "$marker"; then
    echo "Comment with marker '$marker' already exists in discussion $discussion_id. Skipping."
    return 0
  fi

  echo "Posting update to discussion $discussion_id..."
  gh api graphql -F id="$discussion_id" -f body="$body" \
    -f query='mutation($id: ID!, $body: String!) { addDiscussionComment(input: {discussionId: $id, body: $body}) { comment { url } } }' \
    --jq 'if .errors then error(.errors[0].message) else .data.addDiscussionComment.comment.url end'
}

# Update 1: UI Graph Model (#58)
post_comment "D_kwDORxQzBc4AlQoO" \
'### 🚀 Architectural Update: UI Baseline & Angular 21 (Packets 13-20)

The front-end boundary has been significantly advanced recently:

1. **Angular 21 Upgrade:** The `ui/` directory was sequentially upgraded to Angular 21, migrating to the new `@if`/`@for` block control flow and stabilizing tracking IDs (`track run.runId`).
2. **Frontend Contract Seam:** A `FrontendDataService` abstraction was established with explicit mappers. The UI currently toggles between a `MockFrontendDataService` (for offline design) and an `ApiFrontendDataService` (backed by `HttpClient`) via environment files.
3. **Desktop Skeleton:** A minimal Electron shell has been introduced in `desktop/` to host the web build.
4. **Code Contract Guardrails:** A new validation script, `scripts/check_ui_code_contracts.py`, now runs during the `run_tests.sh ui` tier, explicitly enforcing top-of-file intent block headers across all TypeScript files.
' "Architectural Update: UI Baseline & Angular 21"

# Update 2: Backend CLI Entrypoint (#57)
post_comment "D_kwDORxQzBc4AlQoN" \
'### 🚀 Architectural Update: Minimal API Server & Loopback Binding

The CLI boundary has been expanded beyond one-shot batch execution:

1. **Minimal API Server:** A bare-bones HTTP service (`api/server.py`) has been introduced. The example workflow runtime is assembled once at startup and reused across incoming HTTP requests.
2. **Loopback Policy:** The service defaults strictly to `127.0.0.1` for security, requiring explicit `--host` arguments if network exposure is intended.
3. **UI Integration:** This HTTP boundary is the intended target for the `ApiFrontendDataService` layer recently completed in the Angular 21 UI slice, paving the way for full end-to-end integration.
' "Architectural Update: Minimal API Server & Loopback Binding"

# Update 3: Error Handling (#63)
post_comment "D_kwDORxQzBc4AlQoV" \
'### 🚀 Architectural Update: UI State Recovery & HTTP Normalization

Error handling has been expanded across the API and UI boundaries:

1. **HTTP Error Normalization:** The minimal API server now suppresses raw exception leakage, replacing `print`-style traces with stable, client-facing HTTP 500 JSON payloads.
2. **UI Health & Stream Recovery:** The Angular UI now uses `shareReplay` and `catchError` across data streams (e.g., service health polling). If the API fails, the UI gracefully falls back to explicit `offline` or `unknown` state representations, updating the UI status tone badges rather than failing silently or hanging on stale loading states.
' "Architectural Update: UI State Recovery & HTTP Normalization"

echo "Discussions updated successfully."
