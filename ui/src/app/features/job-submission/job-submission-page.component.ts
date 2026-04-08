/**
 * job-submission-page.component.ts intent header.
 *
 * This file is part of the Angular UI slice and exists to keep the
 * route/component/service contract explicit for the current product increment.
 */
import { AsyncPipe, NgFor, NgIf } from '@angular/common';
import { Component, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { BehaviorSubject, catchError, map, of, startWith, switchMap } from 'rxjs';
import { FrontendDataService } from '../../shared/services/frontend-data.service';
import { PageContainerComponent } from '../../shared/ui/page-container.component';
import { PageHeaderComponent } from '../../shared/ui/page-header.component';
import { PanelCardComponent } from '../../shared/ui/panel-card.component';

@Component({
    standalone: true,
    imports: [ReactiveFormsModule, AsyncPipe, PageContainerComponent, PageHeaderComponent, PanelCardComponent],
    template: `
    <mp-page-container>
      <mp-page-header
        title="Job Submission"
        description="Submit a workflow job with validation, clear submission-state transitions, and transport abstraction."
      ></mp-page-header>

      <mp-panel-card>
        <form [formGroup]="form" (ngSubmit)="submit()" class="form-grid">
          <label for="workflow">Workflow</label>
          <select id="workflow" formControlName="workflowId">
            <option value="">Select workflow</option>
            @for (workflow of (workflows$ | async); track workflow.workflowId) {
              <option [value]="workflow.workflowId">{{workflow.title}} (v{{workflow.version}})</option>
            }
          </select>
          @if (form.controls.workflowId.invalid && form.controls.workflowId.touched) {
            <small>Workflow selection is required.</small>
          }

          <label for="reason">Reason</label>
          <input id="reason" formControlName="reason" maxlength="200" />
          @if (form.controls.reason.errors?.['required'] && form.controls.reason.touched) {
            <small>Reason is required.</small>
          }
          @if (form.controls.reason.errors?.['minlength'] && form.controls.reason.touched) {
            <small>Reason must be at least 10 characters.</small>
          }

          <label for="priority">Priority</label>
          <select id="priority" formControlName="priority">
            <option value="low">Low</option>
            <option value="normal">Normal</option>
            <option value="high">High</option>
          </select>

          <button type="submit" [disabled]="form.invalid || (submitVm$ | async)?.state === 'submitting'">Submit Job</button>
        </form>
      </mp-panel-card>

      @if (submitVm$ | async; as vm) {
        <mp-panel-card>
          @if (vm.state === 'idle') {
            <p>Submission is idle. Complete the form and submit when ready.</p>
          } @else if (vm.state === 'submitting') {
            <p>Submitting job request...</p>
          } @else if (vm.state === 'success') {
            <p>Success: {{ vm.message }}</p>
          } @else if (vm.state === 'error') {
            <p>Error: {{ vm.message }}</p>
          }
        </mp-panel-card>
      }
    </mp-page-container>
    `,
    styles: ['.form-grid{display:grid;grid-template-columns:1fr;gap:var(--mp-space-2);}small{color:#ffb9b9;}']
})
export class JobSubmissionPageComponent {
  private readonly fb = inject(FormBuilder);
  private readonly dataService = inject(FrontendDataService);
  private readonly submitSignal$ = new BehaviorSubject(0);

  protected readonly workflows$ = this.dataService.getWorkflowCatalog();

  protected readonly form = this.fb.nonNullable.group({
    workflowId: ['', Validators.required],
    reason: ['', [Validators.required, Validators.minLength(10), Validators.maxLength(200)]],
    priority: ['normal' as const, Validators.required]
  });

  protected readonly submitVm$ = this.submitSignal$.pipe(
    switchMap((count) => {
      if (count === 0) {
        return of({ state: 'idle', message: '' } as const);
      }
      return this.dataService.submitJob(this.form.getRawValue()).pipe(
        map((result) => ({
          state: result.accepted ? ('success' as const) : ('error' as const),
          message: result.message
        })),
        startWith({ state: 'submitting' as const, message: '' }),
        catchError((error: Error) => of({ state: 'error' as const, message: error.message }))
      );
    }),
    startWith({ state: 'idle' as const, message: '' })
  );

  protected submit(): void {
    this.form.markAllAsTouched();
    if (this.form.invalid) {
      return;
    }
    this.submitSignal$.next(this.submitSignal$.value + 1);
  }
}
