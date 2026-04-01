# MagnetarPrometheus Run/Job Models Schema

## 1. Objective

This document outlines the shared schema contract for submitting and inspecting workflow runs.
These models ensure a consistent boundary between the backend execution engine and any future
application surfaces (UI, API, or CLI) interacting with job runs.

This schema explicitly acts as a sibling to the UI Graph Model (`workflow-graph-schema.md`) and maps
directly to the `Run*` models in `sdk/python/src/magnetar_prometheus_sdk/models.py`.

## 2. Core Concepts

A "Run" or "Job" captures the execution lifecycle of a workflow.

- **RunStatus:** An enumeration of states a run can inhabit.
- **RunSubmissionRequest:** The payload required to start a workflow execution.
- **RunResponse:** The immediate acknowledgment of a submission.
- **RunListingItem:** A lightweight summary for listing multiple runs.
- **RunSummary:** A detailed view of a single run, including its final state.

## 3. Schema Definitions

### 3.1 RunStatus

An enumeration describing the current lifecycle phase of a run.

```yaml
type: string
enum:
  - pending
  - running
  - completed
  - failed
  - cancelled
```

### 3.2 RunSubmissionRequest

The payload structure used to trigger a new run.

```yaml
type: object
properties:
  workflow_id:
    type: string
    description: "The unique ID of the workflow to execute"
  workflow_version:
    type: string
    description: "Optional specific version to execute; defaults to latest if omitted"
  input_data:
    type: object
    description: "Dictionary of input arguments required by the workflow"
    default: {}
  tags:
    type: array
    items:
      type: string
    description: "Optional list of tags for searching and categorizing the run"
    default: []
required:
  - workflow_id
```

### 3.3 RunResponse

The structure returned immediately after submitting a run.

```yaml
type: object
properties:
  run_id:
    type: string
    description: "The unique identifier generated for this specific execution"
  workflow_id:
    type: string
    description: "The ID of the workflow being executed"
  status:
    $ref: "#/definitions/RunStatus"
    description: "The initial status of the run (usually 'pending' or 'running')"
  created_at:
    type: string
    format: date-time
    description: "Timestamp when the run was requested"
  message:
    type: string
    description: "Optional descriptive message regarding the submission"
required:
  - run_id
  - workflow_id
  - status
  - created_at
```

### 3.4 RunListingItem

A lightweight summary meant for list views (e.g., a dashboard or CLI table).

```yaml
type: object
properties:
  run_id:
    type: string
  workflow_id:
    type: string
  status:
    $ref: "#/definitions/RunStatus"
  created_at:
    type: string
    format: date-time
  completed_at:
    type: string
    format: date-time
    description: "Timestamp when the run reached a terminal state; null if active"
  tags:
    type: array
    items:
      type: string
    description: "Optional list of tags for searching and categorizing the run"
    default: []
required:
  - run_id
  - workflow_id
  - status
  - created_at
```

### 3.5 RunSummary

The detailed, deep-inspect structure of a single run. Includes the final execution context and any error outputs.

```yaml
type: object
properties:
  run_id:
    type: string
  workflow_id:
    type: string
  status:
    $ref: "#/definitions/RunStatus"
  created_at:
    type: string
    format: date-time
  completed_at:
    type: string
    format: date-time
  tags:
    type: array
    items:
      type: string
    description: "Optional list of tags for searching and categorizing the run"
    default: []
  final_context:
    $ref: "#/definitions/RunContext"
    description: "The aggregated state of the workflow upon completion. (See runtime schema for RunContext definition)"
  error_message:
    type: string
    description: "Top-level error message if the run failed"
required:
  - run_id
  - workflow_id
  - status
  - created_at
```

## 4. Integration Details

### Mapping to the Backend
Currently, `magnetar_prometheus` runs workflows interactively and synchronously via the CLI.
These models prepare the shared contract boundary for the introduction of:
- An asynchronous queue or background worker pool.
- A REST/GraphQL API layer.
- A persistent storage mechanism for run history.

### Mapping to the UI
Future UI development will rely on these models for:
- "Run this workflow" dialogs (compiling into a `RunSubmissionRequest`).
- Job tracking tables (displaying `RunListingItem` objects).
- Detailed run inspectors (visualizing a `RunSummary` and its `final_context`).
