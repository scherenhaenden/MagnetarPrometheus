/**
 * Mock data adapter for the first UI increments.
 *
 * Why keep this explicit instead of hardcoding arrays inside page components:
 * - We need a stable seam for upcoming API mode work under milestone ms-04/ms-05.
 * - Feature slices (run history, job submission) can move independently if they consume
 *   this adapter through the FrontendDataService contract.
 * - The mock keeps the user flow inspectable before the backend HTTP endpoints are complete.
 */
import { Injectable } from '@angular/core';
import { Observable, delay, map, of } from 'rxjs';
import {
  JobSubmissionRequest,
  JobSubmissionResult,
  RunDetail,
  RunListingItem,
  ServiceHealthSnapshot,
  WorkflowSummary
} from '../models/frontend-contracts';
import { FrontendDataService } from './frontend-data.service';

@Injectable()
export class MockFrontendDataService extends FrontendDataService {
  private readonly runHistory: RunListingItem[] = [
    {
      runId: 'run-20260407-001',
      workflowId: 'email-triage',
      status: 'succeeded',
      createdAtIso: '2026-04-07T09:00:00Z',
      completedAtIso: '2026-04-07T09:00:07Z',
      summary: '3 incoming messages triaged with routing decisions.'
    },
    {
      runId: 'run-20260407-002',
      workflowId: 'error-module',
      status: 'failed',
      createdAtIso: '2026-04-07T10:15:00Z',
      completedAtIso: '2026-04-07T10:15:02Z',
      summary: 'Synthetic failure flow confirmed alert behavior.'
    }
  ];

  public getServiceHealth(): Observable<ServiceHealthSnapshot> {
    const healthSnapshot: ServiceHealthSnapshot = {
      status: 'healthy',
      message: 'UI is currently running in mock transport mode.',
      checkedAtIso: new Date().toISOString(),
      mode: 'mock'
    };

    return of(healthSnapshot).pipe(delay(150));
  }

  public getRunHistory(): Observable<ReadonlyArray<RunListingItem>> {
    return of([...this.runHistory]).pipe(delay(250));
  }

  public getRunDetail(runId: string): Observable<RunDetail | null> {
    return this.getRunHistory().pipe(
      map((items) => items.find((item) => item.runId === runId) ?? null),
      map((item) => {
        if (!item) {
          return null;
        }
        return {
          runId: item.runId,
          workflowId: item.workflowId,
          status: item.status,
          createdAtIso: item.createdAtIso,
          completedAtIso: item.completedAtIso,
          steps: [
            { name: 'collect-input', state: 'done', detail: 'Input payload validated and normalized.' },
            { name: 'process-route', state: item.status === 'failed' ? 'failed' : 'done', detail: item.status === 'failed' ? 'Rule evaluation failed in mock branch.' : 'Routing rule selected workflow branch.' },
            { name: 'persist-summary', state: item.status === 'failed' ? 'pending' : 'done', detail: 'Summary persistence placeholder for transport-agnostic UI.' }
          ],
          errorMessage: item.status === 'failed' ? 'Synthetic module failure (mock).' : null,
          outputPreview: item.summary
        };
      })
    );
  }

  public getWorkflowCatalog(): Observable<ReadonlyArray<WorkflowSummary>> {
    return of([
      {
        workflowId: 'email-triage',
        title: 'Email Triage',
        description: 'Classify inbound email traffic and route follow-up actions.',
        tags: ['email', 'support', 'routing'],
        version: '1.2.0'
      },
      {
        workflowId: 'error-module',
        title: 'Failure Simulator',
        description: 'Validate failure handling and observability paths.',
        tags: ['qa', 'failure', 'testing'],
        version: '0.9.0'
      }
    ]);
  }

  public submitJob(request: JobSubmissionRequest): Observable<JobSubmissionResult> {
    const generatedRunId = `run-${Date.now()}`;
    this.runHistory.unshift({
      runId: generatedRunId,
      workflowId: request.workflowId,
      status: 'queued',
      createdAtIso: new Date().toISOString(),
      completedAtIso: null,
      summary: `Queued from UI (${request.priority} priority): ${request.reason}`
    });

    return of({
      accepted: true,
      runId: generatedRunId,
      message: 'Submission accepted by mock adapter. API wiring is the next increment.'
    }).pipe(delay(250));
  }
}
