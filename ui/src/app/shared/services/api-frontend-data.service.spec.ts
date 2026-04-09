/**
 * api-frontend-data.service.spec.ts intent header.
 *
 * This test file validates the ApiFrontendDataService class.
 */
import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ApiFrontendDataService } from './api-frontend-data.service';

describe('ApiFrontendDataService', () => {
  let service: ApiFrontendDataService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        ApiFrontendDataService,
        provideHttpClient(),
        provideHttpClientTesting()
      ]
    });
    service = TestBed.inject(ApiFrontendDataService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should fetch service health and map it to a snapshot', () => {
    service.getServiceHealth().subscribe((snapshot) => {
      expect(snapshot).toEqual({
        status: 'healthy',
        message: 'All good',
        checkedAtIso: '2026-04-09T10:00:00Z',
        mode: 'api'
      });
    });

    const request = httpMock.expectOne('/api/health/status');
    expect(request.request.method).toBe('GET');
    request.flush({
      status: 'healthy',
      message: 'All good',
      checked_at: '2026-04-09T10:00:00Z'
    });
  });

  it('should fetch run history and map each item', () => {
    service.getRunHistory().subscribe((items) => {
      expect(items).toEqual([
        {
          runId: 'run-1',
          workflowId: 'workflow-a',
          status: 'succeeded',
          createdAtIso: '2026-04-09T10:00:00Z',
          completedAtIso: '2026-04-09T10:00:01Z',
          summary: 'Done'
        }
      ]);
    });

    const request = httpMock.expectOne('/api/runs');
    expect(request.request.method).toBe('GET');
    request.flush([
      {
        run_id: 'run-1',
        workflow_id: 'workflow-a',
        status: 'succeeded',
        created_at: '2026-04-09T10:00:00Z',
        completed_at: '2026-04-09T10:00:01Z',
        summary: 'Done'
      }
    ]);
  });

  it('should fetch run detail and map a null response safely', () => {
    service.getRunDetail('run-404').subscribe((detail) => {
      expect(detail).toBeNull();
    });

    const request = httpMock.expectOne('/api/runs/run-404');
    expect(request.request.method).toBe('GET');
    request.flush(null);
  });

  it('should fetch workflow catalog and map version defaults', () => {
    service.getWorkflowCatalog().subscribe((items) => {
      expect(items).toEqual([
        {
          workflowId: 'workflow-a',
          title: 'Workflow A',
          description: 'Description',
          tags: ['alpha'],
          version: 'unversioned'
        }
      ]);
    });

    const request = httpMock.expectOne('/api/workflows');
    expect(request.request.method).toBe('GET');
    request.flush([
      {
        workflow_id: 'workflow-a',
        title: 'Workflow A',
        description: 'Description',
        tags: ['alpha']
      }
    ]);
  });

  it('should submit jobs using the mapped request payload', () => {
    service.submitJob({
      workflowId: 'workflow-a',
      reason: 'Smoke test',
      priority: 'high'
    }).subscribe((result) => {
      expect(result).toEqual({
        accepted: true,
        runId: 'run-123',
        message: 'Accepted'
      });
    });

    const request = httpMock.expectOne('/api/jobs/submit');
    expect(request.request.method).toBe('POST');
    expect(request.request.body).toEqual({
      workflow_id: 'workflow-a',
      reason: 'Smoke test',
      priority: 'high'
    });
    request.flush({
      accepted: true,
      run_id: 'run-123',
      message: 'Accepted'
    });
  });
});
