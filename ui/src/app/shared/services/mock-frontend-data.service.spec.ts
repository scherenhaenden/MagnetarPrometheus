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
});
