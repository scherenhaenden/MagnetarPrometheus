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
  imports: [AsyncPipe, NgFor, NgIf, PageContainerComponent, PageHeaderComponent, PanelCardComponent, DataListWrapperComponent],
  template: `
    <mp-page-container>
      <mp-page-header title="Workflow Catalog" description="Available workflow templates and metadata exposed through the frontend data service boundary."></mp-page-header>
      <ng-container *ngIf="vm$ | async as vm">
        <mp-panel-card *ngIf="vm.loading">Loading workflow catalog...</mp-panel-card>
        <mp-panel-card *ngIf="vm.error">Unable to load workflow catalog: {{ vm.error }}</mp-panel-card>
        <mp-panel-card *ngIf="!vm.loading && !vm.error && vm.items.length===0">No workflows are currently available.</mp-panel-card>
        <mp-data-list-wrapper *ngIf="!vm.loading && !vm.error && vm.items.length > 0">
          <mp-panel-card *ngFor="let workflow of vm.items">
            <strong>{{workflow.title}}</strong> ({{workflow.workflowId}} · v{{workflow.version}})
            <p>{{workflow.description}}</p>
          </mp-panel-card>
        </mp-data-list-wrapper>
      </ng-container>
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
