/**
 * workflow-catalog-page.component.ts intent header.
 *
 * This file is part of the Angular UI slice and exists to keep the
 * route/component/service contract explicit for the current product increment.
 */
import { AsyncPipe, NgFor, NgIf } from '@angular/common';
import { Component, inject } from '@angular/core';
import { catchError, map, of, startWith } from 'rxjs';
import { FrontendDataService } from '../../shared/services/frontend-data.service';
import { DataListWrapperComponent } from '../../shared/ui/data-list-wrapper.component';
import { PageContainerComponent } from '../../shared/ui/page-container.component';
import { PageHeaderComponent } from '../../shared/ui/page-header.component';
import { PanelCardComponent } from '../../shared/ui/panel-card.component';

/**
 * WorkflowCatalogPageComponent is responsible for displaying all available workflows
 * that can be instantiated or interacted with by the user.
 *
 * This component acts as a read-only list view, gathering metadata about workflows
 * from the backend through the FrontendDataService and presenting them in a structured
 * format (cards within a list). It manages loading, error, and empty states robustly.
 */
@Component({
  imports: [AsyncPipe, PageContainerComponent, PageHeaderComponent, PanelCardComponent, DataListWrapperComponent],
  templateUrl: './workflow-catalog-page.component.html'
})
export class WorkflowCatalogPageComponent {
  /**
   * Injects the FrontendDataService, providing the interface to request the catalog data.
   */
  private readonly dataService = inject(FrontendDataService);

  /**
   * The reactive view model for the workflow catalog.
   *
   * How it works:
   * 1. Initiates a call to `getWorkflowCatalog()` on the data service.
   * 2. Maps the successful array of workflow items into a state object `{ items, error, loading }`.
   * 3. Catches any network or service errors, surfacing them as a string in the state object
   *    while keeping the items array empty.
   * 4. Uses `startWith` to emit a loading state immediately before the network request completes,
   *    ensuring the UI can show a loading indicator.
   */
  protected readonly vm$ = this.dataService.getWorkflowCatalog().pipe(
    map((items) => ({ items, error: null as string | null, loading: false })),
    catchError((error: Error) => of({ items: [], error: error.message, loading: false })),
    startWith({ items: [], error: null as string | null, loading: true })
  );
}
