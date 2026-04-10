/**
 * Frontend contract boundary for MagnetarPrometheus.
 *
 * This contract file is intentionally the only domain shape that feature components consume.
 * Backend payloads may evolve, and mock transport may diverge from HTTP payload structure,
 * but the UI surface should remain stable behind these TypeScript interfaces.
 */

/**
 * Represeents the high-level status of a workflow run in the frontend.
 */
export type FrontendRunStatus =
  | 'queued'
  | 'running'
  | 'succeeded'
  | 'failed'
  | 'cancelled'
  | 'unknown';

/**
 * Represents the execution state of an individual step within a run.
 */
export type FrontendStepState = 'pending' | 'done' | 'failed' | 'unknown';

/**
 * A snapshot of the backend service health.
 */
export interface ServiceHealthSnapshot {
  /** The current health status of the backend. */
  readonly status: 'healthy' | 'degraded' | 'offline';
  /** A human-readable message describing the health status. */
  readonly message: string;
  /** ISO timestamp of when the health check was performed. */
  readonly checkedAtIso: string;
  /** The transport mode being used (mock or real API). */
  readonly mode: 'mock' | 'api';
}

/**
 * A summary of a workflow run used in listing views.
 */
export interface RunListingItem {
  /** The unique identifier for the run. */
  readonly runId: string;
  /** The ID of the workflow being executed. */
  readonly workflowId: string;
  /** The current status of the run. */
  readonly status: FrontendRunStatus;
  /** ISO timestamp of when the run was created. */
  readonly createdAtIso: string;
  /** ISO timestamp of when the run completed, or null if still active. */
  readonly completedAtIso: string | null;
  /** A short summary of the run's progress or outcome. */
  readonly summary: string;
}

/**
 * Detailed state of an individual step in a workflow run.
 */
export interface RunDetailStep {
  /** The name of the step. */
  readonly name: string;
  /** The current execution state of this step. */
  readonly state: FrontendStepState;
  /** Detailed information or results from this step's execution. */
  readonly detail: string;
}

/**
 * Full details of a workflow run, including its step-by-step timeline.
 */
export interface RunDetail {
  /** The unique identifier for the run. */
  readonly runId: string;
  /** The ID of the workflow being executed. */
  readonly workflowId: string;
  /** The current status of the run. */
  readonly status: FrontendRunStatus;
  /** ISO timestamp of when the run was created. */
  readonly createdAtIso: string;
  /** ISO timestamp of when the run completed, or null if still active. */
  readonly completedAtIso: string | null;
  /** The timeline of execution steps for this run. */
  readonly steps: ReadonlyArray<RunDetailStep>;
  /** The error message if the run failed, or null otherwise. */
  readonly errorMessage: string | null;
  /** A preview of the final workflow output. */
  readonly outputPreview: string;
}

/**
 * A summary of a workflow definition in the catalog.
 */
export interface WorkflowSummary {
  /** The unique identifier for the workflow. */
  readonly workflowId: string;
  /** A human-readable title for the workflow. */
  readonly title: string;
  /** A description of what the workflow does. */
  readonly description: string;
  /** Searchable tags associated with this workflow. */
  readonly tags: ReadonlyArray<string>;
  /** The version of the workflow definition. */
  readonly version: string;
}

/**
 * Parameters for submitting a new job request.
 */
export interface JobSubmissionRequest {
  /** The ID of the workflow to submit. */
  readonly workflowId: string;
  /** The reason for submitting the job. */
  readonly reason: string;
  /** The execution priority for the new job. */
  readonly priority: 'low' | 'normal' | 'high';
}

/**
 * The outcome of a job submission request.
 */
export interface JobSubmissionResult {
  /** Whether the submission was accepted by the backend. */
  readonly accepted: boolean;
  /** The newly generated run ID if the submission was accepted. */
  readonly runId: string | null;
  /** A response message from the backend regarding the submission. */
  readonly message: string;
}
