/**
 * Frontend Contract Boundary for MagnetarPrometheus.
 *
 * Why this file exists:
 * - The backend runtime models are Python-first and may evolve independently.
 * - The Angular product surface needs a stable, TypeScript-native contract seam so feature
 *   components can remain transport-agnostic and avoid coupling to raw HTTP payload details.
 * - During the current milestone, the UI runs mostly in mock mode. Defining explicit interfaces
 *   here keeps future API integration honest: we can swap adapters without rewriting pages.
 */

export type FrontendRunStatus =
  | 'queued'
  | 'running'
  | 'succeeded'
  | 'failed'
  | 'cancelled';

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

export interface RunDetail {
  readonly runId: string;
  readonly workflowId: string;
  readonly status: FrontendRunStatus;
  readonly createdAtIso: string;
  readonly completedAtIso: string | null;
  readonly steps: ReadonlyArray<{ name: string; state: 'pending' | 'done' | 'failed' }>;
  readonly errorMessage: string | null;
  readonly outputPreview: string;
}

export interface WorkflowSummary {
  readonly workflowId: string;
  readonly title: string;
  readonly description: string;
  readonly tags: ReadonlyArray<string>;
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
