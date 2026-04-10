/**
 * run-detail-page.component.ts intent header.
 *
 * This file is part of the Angular UI slice and exists to keep the
 * route/component/service contract explicit for the current product increment.
 */
import { AsyncPipe, DatePipe, NgFor, NgIf } from '@angular/common';
import { Component, inject } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { catchError, map, of, startWith, switchMap } from 'rxjs';
import { FrontendDataService } from '../../shared/services/frontend-data.service';
import { PageContainerComponent } from '../../shared/ui/page-container.component';
import { PageHeaderComponent } from '../../shared/ui/page-header.component';
import { PanelCardComponent } from '../../shared/ui/panel-card.component';
import { StatusBadgeComponent } from '../../shared/ui/status-badge.component';

/**
 * RunDetailPageComponent presents an in-depth view of a single workflow execution.
 *
 * It is responsible for:
 * - Extracting the `runId` from the current route URL.
 * - Requesting the full details of that run from the backend via the FrontendDataService.
 * - Displaying metadata (timestamps, status), the step timeline, and execution output.
 * - Handling loading and error states securely, ensuring users aren't left on broken pages.
 */
@Component({
  standalone: true,
  imports: [AsyncPipe, DatePipe, RouterLink, PageContainerComponent, PageHeaderComponent, PanelCardComponent, StatusBadgeComponent],
  templateUrl: './run-detail-page.component.html',
  styleUrl: './run-detail-page.component.css'
})
export class RunDetailPageComponent {
  /**
   * Access to the current route parameters, used to extract the runId.
   */
  private readonly route = inject(ActivatedRoute);

  /**
   * The frontend data service abstraction used to fetch run details.
   */
  private readonly dataService = inject(FrontendDataService);

  /**
   * The primary View Model observable for the run detail page.
   *
   * This stream orchestrates the page's reactive state by:
   * 1. Extracting the `runId` from the route parameters.
   * 2. Switching to the `getRunDetail` call from the data service.
   * 3. Mapping the result into a structured state object (detail, error, loading).
   * 4. Catching service-level errors and surfacing them in the UI state.
   * 5. Starting with a 'loading' state to provide immediate visual feedback.
   */
  protected readonly vm$ = this.route.paramMap.pipe(
    switchMap((params) => this.dataService.getRunDetail(params.get('runId') ?? '')),
    map((detail) => ({ detail, error: null as string | null, loading: false })),
    catchError((error: Error) => of({ detail: null, error: error.message, loading: false })),
    startWith({ detail: null, error: null as string | null, loading: true })
  );
}
