import { AsyncPipe, NgFor } from '@angular/common';
import { Component, inject } from '@angular/core';
import { FrontendDataService } from '../../shared/services/frontend-data.service';

@Component({
  standalone: true,
  imports: [AsyncPipe, NgFor],
  template: `<h2>Workflow Catalog</h2><ul><li *ngFor="let workflow of (workflows$ | async)"><strong>{{workflow.title}}</strong> — {{workflow.description}}</li></ul>`
})
export class WorkflowCatalogPageComponent {
  private readonly dataService = inject(FrontendDataService);
  protected readonly workflows$ = this.dataService.getWorkflowCatalog();
}
