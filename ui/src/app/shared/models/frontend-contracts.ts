/**
 * Frontend contract boundary for MagnetarPrometheus.
 *
 * This contract file is intentionally the only domain shape that feature components consume.
 * Backend payloads may evolve, and mock transport may diverge from HTTP payload structure,
 * but the UI surface should remain stable behind these TypeScript interfaces.
 */

export type FrontendRunStatus =
  | 'queued'
  | 'running'
  | 'succeeded'
  | 'failed'
  | 'cancelled';

export type FrontendStepState = 'pending' | 'done' | 'failed' | 'unknown';

export interface ServiceHealthSnapshot {
  readonly status: 'healthy' | 'degraded' | 'offline';
  readonly message: string;
  readonly checkedAtIso: string;
  readonly mode: 'mock' | 'api';
}

export interface RunListingItem {
  readonly runId: string;
  readonly workflowId: string;
  readonly status: FrontendRunStatus;
  readonly createdAtIso: string;
  readonly completedAtIso: string | null;
  readonly summary: string;
}

export interface RunDetailStep {
  readonly name: string;
  readonly state: FrontendStepState;
  readonly detail: string;
}

export interface RunDetail {
  readonly runId: string;
  readonly workflowId: string;
  readonly status: FrontendRunStatus;
  readonly createdAtIso: string;
  readonly completedAtIso: string | null;
  readonly steps: ReadonlyArray<RunDetailStep>;
  readonly errorMessage: string | null;
  readonly outputPreview: string;
}

export interface WorkflowSummary {
  readonly workflowId: string;
  readonly title: string;
  readonly description: string;
  readonly tags: ReadonlyArray<string>;
  readonly version: string;
}

export interface JobSubmissionRequest {
  readonly workflowId: string;
  readonly reason: string;
  readonly priority: 'low' | 'normal' | 'high';
}

export interface JobSubmissionResult {
  readonly accepted: boolean;
  readonly runId: string | null;
  readonly message: string;
}
