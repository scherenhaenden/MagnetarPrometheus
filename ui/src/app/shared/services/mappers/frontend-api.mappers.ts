import {
  FrontendRunStatus,
  FrontendStepState,
  JobSubmissionRequest,
  JobSubmissionResult,
  RunDetail,
  RunListingItem,
  ServiceHealthSnapshot,
  WorkflowSummary
} from '../../models/frontend-contracts';
import {
  HealthApiResponse,
  JobSubmissionApiRequest,
  JobSubmissionApiResponse,
  RunDetailApiResponse,
  RunListItemApiResponse,
  WorkflowSummaryApiResponse
} from '../transport/api-transport.contracts';

const normalizeRunStatus = (value: string): FrontendRunStatus => {
  const normalized = value.toLowerCase();
  if (
    normalized === 'queued' ||
    normalized === 'running' ||
    normalized === 'succeeded' ||
    normalized === 'failed' ||
    normalized === 'cancelled'
  ) {
    return normalized;
  }
  return 'failed';
};

const normalizeStepState = (value: string): FrontendStepState => {
  const normalized = value.toLowerCase();
  if (normalized === 'pending' || normalized === 'done' || normalized === 'failed') {
    return normalized;
  }
  return 'pending';
};

export const mapHealthApiResponseToSnapshot = (
  response: HealthApiResponse,
  mode: 'api' | 'mock'
): ServiceHealthSnapshot => ({
  status: response.status,
  message: response.message,
  checkedAtIso: response.checked_at,
  mode
});

export const mapRunListItemApiResponseToRunListingItem = (
  response: RunListItemApiResponse
): RunListingItem => ({
  runId: response.run_id,
  workflowId: response.workflow_id,
  status: normalizeRunStatus(response.status),
  createdAtIso: response.created_at,
  completedAtIso: response.completed_at,
  summary: response.summary
});

export const mapRunDetailApiResponseToRunDetail = (response: RunDetailApiResponse): RunDetail => ({
  runId: response.run_id,
  workflowId: response.workflow_id,
  status: normalizeRunStatus(response.status),
  createdAtIso: response.created_at,
  completedAtIso: response.completed_at,
  steps: response.steps.map((step) => ({
    name: step.name,
    state: normalizeStepState(step.state),
    detail: step.detail ?? 'No additional step detail returned by API.'
  })),
  errorMessage: response.error_message,
  outputPreview: response.output_preview
});

export const mapWorkflowSummaryApiResponseToWorkflowSummary = (
  response: WorkflowSummaryApiResponse
): WorkflowSummary => ({
  workflowId: response.workflow_id,
  title: response.title,
  description: response.description,
  tags: response.tags,
  version: response.version ?? 'unversioned'
});

export const mapJobSubmissionRequestToApiRequest = (
  request: JobSubmissionRequest
): JobSubmissionApiRequest => ({
  workflow_id: request.workflowId,
  reason: request.reason,
  priority: request.priority
});

export const mapJobSubmissionApiResponseToJobSubmissionResult = (
  response: JobSubmissionApiResponse
): JobSubmissionResult => ({
  accepted: response.accepted,
  runId: response.run_id,
  message: response.message
});
