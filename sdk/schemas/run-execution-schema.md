# MagnetarPrometheus Run and Execution Schema

## 1. Objective

This document defines the language-neutral contract for workflow executions (runs), job submission, and state inspection in MagnetarPrometheus. It bridges the current CLI-based engine reality with the future interactive application surface (API and UI).

While `workflow-graph-schema.md` defines how a workflow is authored, this document defines how a workflow is requested, tracked, and evaluated during and after its execution.

## 2. Core Concepts

*   **Job Submission:** The request to start a workflow execution. It encapsulates the workflow ID, the desired starting context, and execution policies.
*   **Run:** A single, unique execution of a workflow. A run has a unique identifier, a status, and an associated context that evolves as steps are executed.
*   **RunContext:** The current state of a run, containing inputs, intermediate results, AI decisions, execution history, and errors. This directly maps to the backend `RunContext` model.
*   **RunResult Envelope:** The final payload returned when a run completes (successfully or not), providing a summary of the execution alongside the final context.

## 3. Schema Definitions

The schema is defined conceptually using JSON/YAML structures.

### 3.1 Job Submission Schema

A job submission represents a request from a client (UI, CLI, API) to the orchestration engine to start a workflow.

```yaml
definitions:
  JobSubmission:
    type: object
    properties:
      workflow_id:
        type: string
        description: "The unique identifier of the workflow to execute"
      input_data:
        type: object
        description: "Initial data injected into the `input` section of the RunContext"
      options:
        type: object
        description: "Execution policies or overrides"
        properties:
          dry_run:
            type: boolean
            description: "If true, validate and plan without executing side-effects"
            default: false
          trace_level:
            type: string
            enum: ["info", "debug", "trace"]
            default: "info"
```

### 3.2 Run Lifecycle and Status Model

A run progresses through a defined set of statuses. These statuses dictate what operations are permitted on the run (e.g., you can cancel a `running` job, but not a `completed` one).

```yaml
definitions:
  RunStatus:
    type: string
    enum:
      - pending      # Accepted but not yet executing (e.g., queued)
      - running      # Currently executing steps
      - paused       # Execution temporarily halted (e.g., awaiting human review)
      - completed    # Execution finished successfully
      - failed       # Execution halted due to an error
      - cancelled    # Execution aborted by user request
```

### 3.3 RunContext Schema (Maps to `RunContext`)

The `RunContext` represents the state of the workflow at any given point in time. This is the core object passed between steps.

```yaml
definitions:
  RunContext:
    type: object
    properties:
      run:
        type: object
        description: "Metadata about the current execution"
        properties:
          id: { type: string, description: "Unique run identifier" }
          workflow_id: { type: string }
          status: { $ref: "#/definitions/RunStatus" }
          current_step: { type: string, description: "ID of the currently executing or last executed step" }
          start_time: { type: string, format: "date-time" }
          end_time: { type: string, format: "date-time", description: "Null if still running" }
      input:
        type: object
        description: "Read-only input data provided at job submission"
      data:
        type: object
        description: "State modified and read by standard workflow steps"
      ai:
        type: object
        description: "State specifically reserved for AI analysis and decisions"
      history:
        type: array
        description: "Chronological log of executed steps"
        items:
          type: object
          properties:
            step_id: { type: string }
            status: { type: string, enum: ["success", "failed"] }
            duration_ms: { type: number }
            timestamp: { type: string, format: "date-time" }
      errors:
        type: array
        description: "Accumulated errors across the run"
        items:
          type: object
          properties:
            step_id: { type: string }
            error_code: { type: string }
            message: { type: string }
```

### 3.4 RunResult Envelope Schema

When a client queries the final result of a workflow execution, or when an engine completes a run, it returns a `RunResult Envelope`.

```yaml
definitions:
  RunResultEnvelope:
    type: object
    properties:
      run_id:
        type: string
      workflow_id:
        type: string
      status:
        $ref: "#/definitions/RunStatus"
      final_context:
        $ref: "#/definitions/RunContext"
        description: "The complete state of the context at the end of execution"
      summary:
        type: object
        description: "A high-level overview of the execution"
        properties:
          total_steps_executed: { type: number }
          total_duration_ms: { type: number }
          has_errors: { type: boolean }
```

## 4. Client-Engine Interactions (Future API/UI)

The UI or external systems will interact with the engine using these contracts:

### 4.1 Initiating a Run

A client submits a `JobSubmission` payload. The engine responds with an initial `RunContext` (with status `pending` or `running`) or a unique `run_id` to poll.

### 4.2 Inspecting Execution State

A client (like an operator dashboard) queries a specific `run_id` to retrieve the current `RunContext`. The UI can use `RunContext.run.current_step` to highlight the active node on the visual graph, and `RunContext.history` to show the path taken.

### 4.3 Retrieving Run History

A client queries the engine for a list of runs, optionally filtered by `workflow_id` or `status`. The engine returns an array of abbreviated `RunContext.run` metadata objects.

### 4.4 Resuming/Interacting (Future)

If a run is in a `paused` state (e.g., waiting for manual review from a `review.queue` step), a client can submit a continuation payload referencing the `run_id`, injecting new data into the context, and transitioning the status back to `running`.
