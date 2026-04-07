/**
 * job-submission-page.component.spec.ts intent header.
 *
 * This file is part of the Angular UI slice and exists to keep the
 * route/component/service contract explicit for the current product increment.
 */
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { JobSubmissionPageComponent } from './job-submission-page.component';
import { FrontendDataService } from '../../shared/services/frontend-data.service';

class FrontendDataServiceStub {
  getServiceHealth() {
    return of({ status: 'healthy', message: 'ok', checkedAtIso: '2026-04-07T00:00:00Z', mode: 'mock' as const });
  }

  getRunHistory() {
    return of([]);
  }

  getRunDetail() {
    return of(null);
  }

  getWorkflowCatalog() {
    return of([
      {
        workflowId: 'email-triage',
        title: 'Email Triage',
        description: 'desc',
        tags: [],
        version: '1.0'
      }
    ]);
  }

  submitJob() {
    return of({ accepted: true, runId: 'run-1', message: 'ok' });
  }
}

describe('JobSubmissionPageComponent', () => {
  let fixture: ComponentFixture<JobSubmissionPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [JobSubmissionPageComponent],
      providers: [{ provide: FrontendDataService, useClass: FrontendDataServiceStub }]
    }).compileComponents();

    fixture = TestBed.createComponent(JobSubmissionPageComponent);
    fixture.detectChanges();
  });

  it('marks workflow and reason fields as required', () => {
    const component = fixture.componentInstance;
    component['form'].setValue({ workflowId: '', reason: '', priority: 'normal' });
    expect(component['form'].invalid).toBeTrue();
  });
});
