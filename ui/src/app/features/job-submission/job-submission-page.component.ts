/**
 * Job submission feature slice.
 */
import { AsyncPipe, JsonPipe, NgFor, NgIf } from '@angular/common';
import { Component, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Subject, switchMap } from 'rxjs';
import { FrontendDataService } from '../../shared/services/frontend-data.service';

@Component({
  standalone: true,
  imports: [ReactiveFormsModule, NgFor, NgIf, AsyncPipe, JsonPipe],
  template: `
    <section>
      <h2>Submit Job</h2>
      <form [formGroup]="form" (ngSubmit)="submit()">
        <label>Workflow</label>
        <select formControlName="workflowId">
          <option *ngFor="let workflow of (workflows$ | async)" [value]="workflow.workflowId">{{workflow.title}}</option>
        </select>
        <label>Reason</label>
        <input formControlName="reason" />
        <label>Priority</label>
        <select formControlName="priority">
          <option value="low">Low</option>
          <option value="normal">Normal</option>
          <option value="high">High</option>
        </select>
        <button type="submit" [disabled]="form.invalid">Submit</button>
      </form>

      <pre *ngIf="result$ | async as result">{{ result | json }}</pre>
    </section>
  `
})
export class JobSubmissionPageComponent {
  private readonly fb = inject(FormBuilder);
  private readonly dataService = inject(FrontendDataService);
  private readonly submitSignal$ = new Subject<void>();

  protected readonly workflows$ = this.dataService.getWorkflowCatalog();

  protected readonly form = this.fb.nonNullable.group({
    workflowId: ['email-triage', Validators.required],
    reason: ['Manual operator run from web UI shell', [Validators.required, Validators.minLength(8)]],
    priority: ['normal' as const, Validators.required]
  });

  protected readonly result$ = this.submitSignal$.pipe(
    switchMap(() => this.dataService.submitJob(this.form.getRawValue()))
  );

  protected submit(): void {
    if (this.form.invalid) {
      return;
    }
    this.submitSignal$.next();
  }
}
