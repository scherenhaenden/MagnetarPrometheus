/**
 * frontend-api.mappers.spec.ts intent header.
 *
 * This test file validates mapping functions in frontend-api.mappers.
 */
import { mapHealthApiResponseToSnapshot } from './frontend-api.mappers';
import {
  mapJobSubmissionApiResponseToJobSubmissionResult,
  mapJobSubmissionRequestToApiRequest,
  mapRunDetailApiResponseToRunDetail,
  mapRunListItemApiResponseToRunListingItem,
  mapWorkflowSummaryApiResponseToWorkflowSummary
} from './frontend-api.mappers';

describe('Frontend API Mappers', () => {
  describe('mapHealthApiResponseToSnapshot', () => {
    it('should map correctly', () => {
      const response = {
        status: 'healthy' as const,
        message: 'All good',
        checked_at: '2026-01-01T00:00:00Z'
      };

      const snapshot = mapHealthApiResponseToSnapshot(response, 'api');

      expect(snapshot.status).toBe('healthy');
      expect(snapshot.message).toBe('All good');
      expect(snapshot.checkedAtIso).toBe('2026-01-01T00:00:00Z');
      expect(snapshot.mode).toBe('api');
    });
  });

  describe('mapRunListItemApiResponseToRunListingItem', () => {
    it('should normalize unknown run statuses to failed', () => {
      expect(mapRunListItemApiResponseToRunListingItem({
        run_id: 'run-1',
        workflow_id: 'workflow-a',
        status: 'unexpected',
        created_at: '2026-01-01T00:00:00Z',
        completed_at: null,
        summary: 'Summary'
      })).toEqual({
        runId: 'run-1',
        workflowId: 'workflow-a',
        status: 'failed',
        createdAtIso: '2026-01-01T00:00:00Z',
        completedAtIso: null,
        summary: 'Summary'
      });
    });
  });

  describe('mapRunDetailApiResponseToRunDetail', () => {
    it('should map step detail defaults and normalize states', () => {
      expect(mapRunDetailApiResponseToRunDetail({
        run_id: 'run-1',
        workflow_id: 'workflow-a',
        status: 'succeeded',
        created_at: '2026-01-01T00:00:00Z',
        completed_at: '2026-01-01T00:00:01Z',
        steps: [
          { name: 'step-1', state: 'done' },
          { name: 'step-2', state: 'mystery', detail: 'Provided detail' }
        ],
        error_message: null,
        output_preview: 'Preview'
      })).toEqual({
        runId: 'run-1',
        workflowId: 'workflow-a',
        status: 'succeeded',
        createdAtIso: '2026-01-01T00:00:00Z',
        completedAtIso: '2026-01-01T00:00:01Z',
        steps: [
          { name: 'step-1', state: 'done', detail: 'No additional step detail returned by API.' },
          { name: 'step-2', state: 'unknown', detail: 'Provided detail' }
        ],
        errorMessage: null,
        outputPreview: 'Preview'
      });
    });
  });

  describe('mapWorkflowSummaryApiResponseToWorkflowSummary', () => {
    it('should default the version when omitted', () => {
      expect(mapWorkflowSummaryApiResponseToWorkflowSummary({
        workflow_id: 'workflow-a',
        title: 'Workflow A',
        description: 'Description',
        tags: ['alpha']
      })).toEqual({
        workflowId: 'workflow-a',
        title: 'Workflow A',
        description: 'Description',
        tags: ['alpha'],
        version: 'unversioned'
      });
    });
  });

  describe('mapJobSubmissionRequestToApiRequest', () => {
    it('should map the request to API shape', () => {
      expect(mapJobSubmissionRequestToApiRequest({
        workflowId: 'workflow-a',
        reason: 'Reason',
        priority: 'normal'
      })).toEqual({
        workflow_id: 'workflow-a',
        reason: 'Reason',
        priority: 'normal'
      });
    });
  });

  describe('mapJobSubmissionApiResponseToJobSubmissionResult', () => {
    it('should map the response to frontend result', () => {
      expect(mapJobSubmissionApiResponseToJobSubmissionResult({
        accepted: true,
        run_id: 'run-1',
        message: 'Accepted'
      })).toEqual({
        accepted: true,
        runId: 'run-1',
        message: 'Accepted'
      });
    });
  });
});
