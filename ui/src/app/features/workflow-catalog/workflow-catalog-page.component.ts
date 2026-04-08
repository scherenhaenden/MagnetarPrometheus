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

@Component({
    standalone: true,
    imports: [AsyncPipe, PageContainerComponent, PageHeaderComponent, PanelCardComponent, DataListWrapperComponent],
    template: `
    <mp-page-container>
      <mp-page-header title="Workflow Catalog" description="Available workflow templates and metadata exposed through the frontend data service boundary."></mp-page-header>
      @if (vm$ | async; as vm) {
        @if (vm.loading) {
          <mp-panel-card>Loading workflow catalog...</mp-panel-card>
        } @else if (vm.error) {
          <mp-panel-card>Unable to load workflow catalog: {{ vm.error }}</mp-panel-card>
        } @else if (vm.items.length===0) {
          <mp-panel-card>No workflows are currently available.</mp-panel-card>
        } @else {
          <mp-data-list-wrapper>
            @for (workflow of vm.items; track workflow.workflowId) {
              <mp-panel-card>
                <strong>{{workflow.title}}</strong> ({{workflow.workflowId}} · v{{workflow.version}})
                <p>{{workflow.description}}</p>
              </mp-panel-card>
            }
          </mp-data-list-wrapper>
        }
      }
    </mp-page-container>
    `
})
export class WorkflowCatalogPageComponent {
  private readonly dataService = inject(FrontendDataService);
  protected readonly vm$ = this.dataService.getWorkflowCatalog().pipe(
    map((items) => ({ items, error: null as string | null, loading: false })),
    catchError((error: Error) => of({ items: [], error: error.message, loading: false })),
    startWith({ items: [], error: null as string | null, loading: true })
  );
}
