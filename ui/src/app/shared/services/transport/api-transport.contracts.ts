/**
 * Raw API transport payload contracts.
 *
 * These interfaces intentionally represent backend-facing wire contracts and should not leak
 * into page components. Mapper functions translate these payloads into frontend view models.
 */

export interface HealthApiResponse {
  readonly status: 'healthy' | 'degraded' | 'offline';
  readonly message: string;
  readonly checked_at: string;
}

export interface RunListItemApiResponse {
  readonly run_id: string;
  readonly workflow_id: string;
  readonly status: string;
  readonly created_at: string;
  readonly completed_at: string | null;
  readonly summary: string;
}

export interface RunDetailApiResponse {
  readonly run_id: string;
  readonly workflow_id: string;
  readonly status: string;
  readonly created_at: string;
  readonly completed_at: string | null;
  readonly steps: ReadonlyArray<{
    name: string;
    state: string;
    detail?: string;
  }>;
  readonly error_message: string | null;
  readonly output_preview: string;
}

export interface WorkflowSummaryApiResponse {
  readonly workflow_id: string;
  readonly title: string;
  readonly description: string;
  readonly tags: ReadonlyArray<string>;
  readonly version?: string;
}

export interface JobSubmissionApiRequest {
  readonly workflow_id: string;
  readonly reason: string;
  readonly priority: 'low' | 'normal' | 'high';
}

export interface JobSubmissionApiResponse {
  readonly accepted: boolean;
  readonly run_id: string | null;
  readonly message: string;
}
