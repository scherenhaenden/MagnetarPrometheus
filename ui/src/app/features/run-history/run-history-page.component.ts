/**
 * run-history-page.component.ts intent header.
 *
 * This file is part of the Angular UI slice and exists to keep the
 * route/component/service contract explicit for the current product increment.
 */
import { AsyncPipe, DatePipe, NgFor, NgIf } from '@angular/common';
import { Component, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { catchError, combineLatest, map, of, startWith } from 'rxjs';
import { FrontendDataService } from '../../shared/services/frontend-data.service';
import { DataListWrapperComponent } from '../../shared/ui/data-list-wrapper.component';
import { PageContainerComponent } from '../../shared/ui/page-container.component';
import { PageHeaderComponent } from '../../shared/ui/page-header.component';
import { PanelCardComponent } from '../../shared/ui/panel-card.component';
import { StatusBadgeComponent } from '../../shared/ui/status-badge.component';

/**
 * RunHistoryPageComponent displays a list of recent workflow executions.
 *
 * It provides users with visibility into past and currently executing jobs.
 * Features include:
 * - Fetching run history from the backend via FrontendDataService.
 * - Reactive filtering by workflow/run ID (text search) and run status (dropdown).
 * - Displaying loading, error, and empty states appropriately.
 *
 * The component relies heavily on RxJS to combine the stream of data from the server
 * with the stream of values from the filter form, ensuring the UI always reflects
 * the data filtered by the most recent user criteria.
 */
@Component({
  imports: [
    AsyncPipe,
    DatePipe,
    RouterLink,
    ReactiveFormsModule,
    PageContainerComponent,
    PageHeaderComponent,
    PanelCardComponent,
    DataListWrapperComponent,
    StatusBadgeComponent
  ],
  templateUrl: './run-history-page.component.html',
  styleUrl: './run-history-page.component.css'
})
export class RunHistoryPageComponent {
  /**
   * Injects the FrontendDataService to fetch run history records.
   */
  private readonly dataService = inject(FrontendDataService);

  /**
   * Injects FormBuilder to construct the reactive filter form.
   */
  private readonly fb = inject(FormBuilder);

  /**
   * Reactive form group for the run history filters.
   * `nonNullable` ensures that resetting the form (or parts of it)
   * falls back to these initial values instead of `null`, simplifying type safety.
   */
  protected readonly filterForm = this.fb.nonNullable.group({
    search: '',
    status: 'all'
  });

  /**
   * An observable stream representing the current values of the filter form.
   * `startWith` primes the stream with the initial form values so that `combineLatest`
   * emits immediately upon subscription instead of waiting for the user to change a filter.
   */
  private readonly filterValue$ = this.filterForm.valueChanges.pipe(
    map(() => this.filterForm.getRawValue()),
    startWith(this.filterForm.getRawValue())
  );

  /**
   * The core view-model observable for the component.
   *
   * This observable orchestrates the logic:
   * 1. Fetches run history data. If it fails, catches the error and surfaces it in the state.
   * 2. Combines the data stream with the `filterValue$` stream using `combineLatest`.
   * 3. Whenever either the data or the filter changes, it recalculates the filtered list of items.
   * 4. Maps the result into a cohesive view-model object `{ items, error, loading }`
   *    that the template can easily consume via the `async` pipe.
   * 5. Uses `startWith` to emit an initial 'loading' state while the network request is pending.
   */
  protected readonly vm$ = combineLatest([
    this.dataService.getRunHistory().pipe(
      map((items) => ({ items, error: null as string | null })),
      catchError((error: Error) => of({ items: [], error: error.message }))
    ),
    this.filterValue$
  ]).pipe(
    map(([response, filter]) => {
      // The form is built with `nonNullable`, so filter values stay as strings instead of
      // drifting to null during reset or patch flows.
      const query = filter.search.toLowerCase();
      const status = filter.status;

      // Filter the items based on the criteria
      const filtered = response.items.filter((item) => {
        const searchMatches =
          query.length === 0 ||
          item.runId.toLowerCase().includes(query) ||
          item.workflowId.toLowerCase().includes(query);
        const statusMatches = status === 'all' || item.status === status;
        return searchMatches && statusMatches;
      });

      // Return the newly calculated view-model state
      return { items: filtered, error: response.error, loading: false };
    }),
    // Initial state before `combineLatest` emits its first value
    startWith({ items: [], error: null as string | null, loading: true })
  );
}
