/**
 * job-submission-page.component.spec.ts intent header.
 *
 * This file is part of the Angular UI slice and exists to keep the
 * route/component/service contract explicit for the current product increment.
 */
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { firstValueFrom, of, throwError } from 'rxjs';
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

  submitJob(_request?: unknown) {
    return of({ accepted: true, runId: 'run-1', message: 'ok' });
  }
}

describe('JobSubmissionPageComponent', () => {
  let fixture: ComponentFixture<JobSubmissionPageComponent>;
  let component: JobSubmissionPageComponent;
  let service: FrontendDataServiceStub;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [JobSubmissionPageComponent],
      providers: [{ provide: FrontendDataService, useClass: FrontendDataServiceStub }]
    }).compileComponents();

    fixture = TestBed.createComponent(JobSubmissionPageComponent);
    component = fixture.componentInstance;
    service = TestBed.inject(FrontendDataService) as unknown as FrontendDataServiceStub;
    fixture.detectChanges();
  });

  it('marks workflow and reason fields as required', () => {
    component['form'].setValue({ workflowId: '', reason: '', priority: 'normal' });
    expect(component['form'].invalid).toBeTrue();
  });

  it('starts in the idle submit state', async () => {
    await expectAsync(firstValueFrom(component['submitVm$'])).toBeResolvedTo({
      state: 'idle',
      message: ''
    });
  });

  it('exposes the workflow catalog for the select control', async () => {
    await expectAsync(firstValueFrom(component['workflows$'])).toBeResolvedTo([
      jasmine.objectContaining({
        workflowId: 'email-triage',
        title: 'Email Triage'
      })
    ]);
  });

  it('does not submit when the form is invalid', () => {
    spyOn(service, 'submitJob').and.callThrough();

    component['form'].setValue({ workflowId: '', reason: '', priority: 'normal' });
    component['submit']();

    expect(service.submitJob).not.toHaveBeenCalled();
    expect(component['form'].touched).toBeTrue();
  });

  it('submits a valid form and exposes a success state', async () => {
    spyOn(service, 'submitJob').and.callThrough();

    const states: Array<{ state: string; message: string }> = [];
    const subscription = component['submitVm$'].subscribe((value) => {
      states.push(value);
    });

    component['form'].setValue({
      workflowId: 'email-triage',
      reason: 'Valid reason text for coverage.',
      priority: 'normal'
    });
    component['submit']();

    expect(service.submitJob).toHaveBeenCalledWith({
      workflowId: 'email-triage',
      reason: 'Valid reason text for coverage.',
      priority: 'normal'
    });
    expect(states).toContain(jasmine.objectContaining({ state: 'submitting', message: '' }));
    expect(states).toContain(jasmine.objectContaining({ state: 'success', message: 'ok' }));
    subscription.unsubscribe();
  });

  it('exposes an error state when submission fails', async () => {
    spyOn(service, 'submitJob').and.returnValue(
      throwError(() => new Error('submit exploded'))
    );

    component['form'].setValue({
      workflowId: 'email-triage',
      reason: 'Valid reason text for failure.',
      priority: 'normal'
    });
    component['submit']();

    const states: Array<{ state: string; message: string }> = [];
    const subscription = component['submitVm$'].subscribe((value) => {
      states.push(value);
    });

    expect(states).toContain(jasmine.objectContaining({ state: 'submitting', message: '' }));
    expect(states).toContain(jasmine.objectContaining({ state: 'error', message: 'submit exploded' }));
    subscription.unsubscribe();
  });

  it('maps a rejected submission response to the error state', () => {
    spyOn(service, 'submitJob').and.returnValue(
      of({ accepted: false, runId: 'run-2', message: 'rejected by policy' })
    );

    const states: Array<{ state: string; message: string }> = [];
    const subscription = component['submitVm$'].subscribe((value) => {
      states.push(value);
    });

    component['form'].setValue({
      workflowId: 'email-triage',
      reason: 'Valid reason text for rejection.',
      priority: 'normal'
    });
    component['submit']();

    expect(states).toContain(jasmine.objectContaining({ state: 'submitting', message: '' }));
    expect(states).toContain(jasmine.objectContaining({ state: 'error', message: 'rejected by policy' }));
    subscription.unsubscribe();
  });
});
