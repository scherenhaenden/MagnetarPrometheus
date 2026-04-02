# MagnetarPrometheus Run and Execution Schema

## 1. Objective

This document defines the language-neutral contract for workflow executions (runs), job submission, and state inspection in MagnetarPrometheus. It bridges the current CLI-based engine reality with the future interactive application surface (API and UI).

While `workflow-graph-schema.md` defines how a workflow is authored, this document defines how a workflow is requested, tracked, and evaluated during and after its execution.

## 2. Core Concepts

*   **Job Submission:** The request to start a workflow execution. It encapsulates the workflow ID, the desired starting context, and execution policies.
*   **Run:** A single, unique execution of a workflow. A run has a unique identifier, a status, and an associated context that evolves as steps are executed.
*   **RunContext:** The current state of a run, containing inputs, intermediate results, AI decisions, execution history, and errors. This document describes the **target external contract (vNext)** for API/UI consumers; the current backend runtime shape is close in intent but still requires a compatibility mapping layer.
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

### 3.2 Run Lifecycle and Status Model (Target)

A run progresses through a defined set of statuses. These statuses dictate what operations are permitted on the run (e.g., you can cancel a `running` job, but not a `completed` one).

> Compatibility note: the current engine actively emits `running`, `failed`, and `completed`.
> `pending`, `paused`, and `cancelled` are reserved/planned states for future API/runtime capabilities and should not be assumed to exist in the live in-process engine yet.

```yaml
definitions:
  RunStatus:
    type: string
    enum:
      - pending      # Reserved/planned: accepted but not yet executing (e.g., queued)
      - running      # Active: currently executing steps
      - paused       # Reserved/planned: execution temporarily halted (e.g., awaiting human review)
      - completed    # Active: execution finished successfully
      - failed       # Active: execution halted due to an error
      - cancelled    # Reserved/planned: execution aborted by user request
```

### 3.3 RunContext Schema (Target Contract With Runtime Mapping Notes)

The `RunContext` represents the current state of the workflow and is the core object passed between steps.

Compatibility notes for current runtime consumers:

- The in-process engine currently guarantees `run.workflow_id` and `run.status`, but does not yet populate every future-facing metadata field in this target contract (`run.id`, `run.current_step`, `run.start_time`, `run.end_time`) in a durable API-ready way.
- Current runtime `history` entries are emitted as `{step, success, output, error_code, error_message}`. An adapter layer should map those internal records into the target external shape documented below, especially `step -> step_id` and `success -> status`.
- Current runtime `errors` entries are emitted as `{step, error_code, error_message}`. An adapter layer should map those internal records into the target external shape documented below, especially `step -> step_id` and `error_message -> message`.

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
          end_time:
            oneOf:
              - type: string
                format: "date-time"
              - type: "null"
            description: "Null if still running"
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
            status:
              type: string
              enum: ["success", "failed"]
              description: "Per-step outcome, intentionally narrower than the run-level lifecycle enum"
            output:
              type: object
              description: "Per-step output payload retained for traceability and debugging"
            error_code: { type: string }
            error_message: { type: string }
            duration_ms: { type: integer }
            timestamp: { type: string, format: "date-time" }
      errors:
        type: array
        description: "Accumulated errors across the run"
        items:
          type: object
          properties:
            step_id: { type: string }
            error_code: { type: string }
            message:
              type: string
              description: "External contract field; current runtime emits `error_message` and should map it here"
```

### 3.4 RunResult Envelope Schema

When a client queries the final result of a workflow execution through a future API layer, that API can wrap the engine output in a `RunResult Envelope`. The current in-process engine returns the `RunContext` directly, so this envelope should be read as an external-service contract rather than a claim about the exact return shape of `Engine.run(...)` today.

The top-level `run_id`, `workflow_id`, and `status` fields are intentionally duplicated from `final_context.run.*` for client convenience. API consumers can inspect the envelope header without traversing the full nested context object, while still treating `final_context` as the authoritative detailed payload.

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
          total_steps_executed: { type: integer }
          total_duration_ms: { type: integer }
          has_errors: { type: boolean }
```

## 4. Client-Engine Interactions (Future API/UI)

The UI or external systems will interact with the engine using these contracts:

### 4.1 Initiating a Run

A client submits a `JobSubmission` payload. The target API/runtime responds with an initial `RunContext` (with status `pending` or `running`) or a unique `run_id` to poll. In the current in-process engine, workflow execution is immediate and does not yet expose a queued `pending` phase.

### 4.2 Inspecting Execution State

A client (like an operator dashboard) queries a specific `run_id` to retrieve the current `RunContext`. The UI can use `RunContext.run.current_step` to highlight the active node on the visual graph, and `RunContext.history` to show the path taken.

### 4.3 Retrieving Run History

A client queries the engine for a list of runs, optionally filtered by `workflow_id` or `status`. The engine returns an array of abbreviated `RunContext.run` metadata objects.

### 4.4 Resuming/Interacting (Future)

If a run is in a `paused` state (e.g., waiting for manual review from a `review.queue` step), a client can submit a continuation payload referencing the `run_id`, injecting new data into the context, and transitioning the status back to `running`. This is a planned interaction pattern for the future service/API surface rather than a capability emitted by the current engine implementation.
