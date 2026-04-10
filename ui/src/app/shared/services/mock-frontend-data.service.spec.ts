/**
 * mock-frontend-data.service.spec.ts intent header.
 *
 * This test file validates the MockFrontendDataService class.
 */
import { TestBed } from '@angular/core/testing';
import { firstValueFrom } from 'rxjs';
import { MockFrontendDataService } from './mock-frontend-data.service';

describe('MockFrontendDataService', () => {
  let service: MockFrontendDataService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [MockFrontendDataService]
    });
    service = TestBed.inject(MockFrontendDataService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should return seeded run history', async () => {
    await expectAsync(firstValueFrom(service.getRunHistory())).toBeResolvedTo([
      jasmine.objectContaining({ runId: 'run-20260407-001', status: 'succeeded' }),
      jasmine.objectContaining({ runId: 'run-20260407-002', status: 'failed' })
    ]);
  });

  it('should report healthy mock transport status', async () => {
    await expectAsync(firstValueFrom(service.getServiceHealth())).toBeResolvedTo(
      jasmine.objectContaining({
        status: 'healthy',
        mode: 'mock',
        message: 'UI is currently running in mock transport mode.'
      })
    );
  });

  it('should generate run detail for a known run', async () => {
    await expectAsync(firstValueFrom(service.getRunDetail('run-20260407-001'))).toBeResolvedTo(
      jasmine.objectContaining({
        runId: 'run-20260407-001',
        status: 'succeeded',
        steps: jasmine.arrayContaining([
          jasmine.objectContaining({ name: 'collect-input', state: 'done' })
        ])
      })
    );
  });

  it('should include failure detail when generating a failed run detail', async () => {
    await expectAsync(firstValueFrom(service.getRunDetail('run-20260407-002'))).toBeResolvedTo(
      jasmine.objectContaining({
        runId: 'run-20260407-002',
        status: 'failed',
        errorMessage: 'Synthetic module failure (mock).',
        steps: jasmine.arrayContaining([
          jasmine.objectContaining({
            name: 'process-route',
            state: 'failed',
            detail: 'Rule evaluation failed in mock branch.'
          }),
          jasmine.objectContaining({
            name: 'persist-summary',
            state: 'pending'
          })
        ])
      })
    );
  });

  it('should return null for an unknown run detail', async () => {
    await expectAsync(firstValueFrom(service.getRunDetail('missing'))).toBeResolvedTo(null);
  });

  it('should prepend a queued run when submitting a job', async () => {
    const before = await firstValueFrom(service.getRunHistory());

    await expectAsync(firstValueFrom(service.submitJob({
      workflowId: 'email-triage',
      reason: 'Smoke test',
      priority: 'high'
    }))).toBeResolvedTo(jasmine.objectContaining({
      accepted: true,
      message: 'Submission accepted by mock adapter. API wiring is the next increment.'
    }));

    const after = await firstValueFrom(service.getRunHistory());
    expect(after.length).toBe(before.length + 1);
    expect(after[0]).toEqual(jasmine.objectContaining({
      workflowId: 'email-triage',
      status: 'queued',
      summary: 'Queued from UI (high priority): Smoke test'
    }));
  });

  it('should expose the mock workflow catalog', async () => {
    await expectAsync(firstValueFrom(service.getWorkflowCatalog())).toBeResolvedTo([
      jasmine.objectContaining({
        workflowId: 'email-triage',
        title: 'Email Triage',
        version: '1.2.0'
      }),
      jasmine.objectContaining({
        workflowId: 'error-module',
        title: 'Failure Simulator',
        version: '0.9.0'
      })
    ]);
  });
});
