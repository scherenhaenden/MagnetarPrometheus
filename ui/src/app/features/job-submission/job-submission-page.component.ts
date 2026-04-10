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

/**
 * JobSubmissionPageComponent provides a form interface for users to manually trigger new workflow runs.
 *
 * Responsibilities include:
 * - Fetching the list of available workflows to populate a dropdown selection.
 * - Managing a reactive form for job parameters (workflow ID, reason, priority) with built-in validation.
 * - Orchestrating the submission process, cleanly transitioning through states: idle, submitting, success, error.
 * - Disabling submission when the form is invalid or a request is currently in flight.
 */
@Component({
  imports: [ReactiveFormsModule, AsyncPipe, PageContainerComponent, PageHeaderComponent, PanelCardComponent],
  templateUrl: './job-submission-page.component.html',
  styleUrl: './job-submission-page.component.css'
})
export class JobSubmissionPageComponent {
  /**
   * FormBuilder is used to declaratively define the structure and validation rules of the form.
   */
  private readonly fb = inject(FormBuilder);

  /**
   * FrontendDataService is injected to fetch workflows and submit the resulting job request to the backend.
   */
  private readonly dataService = inject(FrontendDataService);

  /**
   * A BehaviorSubject that acts as a trigger for the submission process.
   * It holds a numerical value acting as a counter. Every time the form is successfully submitted,
   * this counter is incremented, signaling the `submitVm$` pipeline to execute a new request.
   * A value of 0 indicates the initial 'idle' state.
   */
  private readonly submitSignal$ = new BehaviorSubject(0);

  /**
   * Observable stream that fetches the catalog of workflows to populate the "Workflow" `<select>` element.
   */
  protected readonly workflows$ = this.dataService.getWorkflowCatalog();

  /**
   * The reactive form model defining the schema for a job submission.
   * `nonNullable` is used to enforce that resetting the form reverts to the defined default values
   * instead of `null`, providing stronger type safety.
   */
  protected readonly form = this.fb.nonNullable.group({
    workflowId: ['', Validators.required],
    reason: ['', [Validators.required, Validators.minLength(10), Validators.maxLength(200)]],
    priority: ['normal' as const, Validators.required]
  });

  /**
   * A reactive view-model that handles the entire lifecycle of a job submission.
   *
   * Flow:
   * 1. Listens to `submitSignal$`.
   * 2. If the signal is 0, it outputs an 'idle' state.
   * 3. When the signal increments (meaning a submission was triggered), it maps the raw form values
   *    and initiates a `submitJob` request via the data service.
   * 4. While the request is pending, it yields a 'submitting' state (via the inner `startWith`).
   * 5. Upon receiving a result, it determines success or error and maps to the appropriate state.
   * 6. It catches network or service errors and yields an 'error' state, preventing the stream from dying.
   */
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

  /**
   * Triggered when the user clicks the submit button.
   *
   * It forces all form controls to be marked as touched, which immediately reveals any validation
   * errors in the UI. If the form passes validation, it increments the `submitSignal$`, which in turn
   * kicks off the `submitVm$` observable pipeline.
   */
  protected submit(): void {
    this.form.markAllAsTouched();
    if (this.form.invalid) {
      return;
    }
    this.submitSignal$.next(this.submitSignal$.value + 1);
  }
}
