import { AsyncPipe, DatePipe, NgFor, NgIf } from '@angular/common';
import { Component, inject } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { catchError, map, of, startWith, switchMap } from 'rxjs';
import { FrontendDataService } from '../../shared/services/frontend-data.service';
import { PageContainerComponent } from '../../shared/ui/page-container.component';
import { PageHeaderComponent } from '../../shared/ui/page-header.component';
import { PanelCardComponent } from '../../shared/ui/panel-card.component';
import { StatusBadgeComponent } from '../../shared/ui/status-badge.component';

@Component({
  standalone: true,
  imports: [AsyncPipe, NgFor, NgIf, DatePipe, RouterLink, PageContainerComponent, PageHeaderComponent, PanelCardComponent, StatusBadgeComponent],
  template: `
    <mp-page-container>
      <mp-page-header
        title="Run Detail"
        description="Inspect selected run metadata, step timeline, and execution output preview."
      ></mp-page-header>

      <ng-container *ngIf="vm$ | async as vm">
        <mp-panel-card *ngIf="vm.loading">Loading run detail...</mp-panel-card>
        <mp-panel-card *ngIf="vm.error">Unable to load run detail: {{ vm.error }}</mp-panel-card>
        <mp-panel-card *ngIf="!vm.loading && !vm.error && !vm.detail">No run found for the selected identifier.</mp-panel-card>

        <ng-container *ngIf="!vm.loading && !vm.error && vm.detail as detail">
          <mp-panel-card>
            <div class="headline"><strong>{{ detail.runId }}</strong><mp-status-badge [text]="detail.status" [tone]="detail.status"></mp-status-badge></div>
            <p>Workflow: {{ detail.workflowId }}</p>
            <p>Created: {{ detail.createdAtIso | date:'medium' }}</p>
            <p *ngIf="detail.completedAtIso">Completed: {{ detail.completedAtIso | date:'medium' }}</p>
            <p *ngIf="detail.errorMessage">Error: {{ detail.errorMessage }}</p>
            <p>Output preview: {{ detail.outputPreview }}</p>
          </mp-panel-card>

          <mp-panel-card>
            <h3>Step Timeline</h3>
            <ul>
              <li *ngFor="let step of detail.steps">
                <strong>{{ step.name }}</strong> — {{ step.state }} — {{ step.detail }}
              </li>
            </ul>
            <a routerLink="/runs">Back to run history</a>
          </mp-panel-card>
        </ng-container>
      </ng-container>
    </mp-page-container>
  `,
  styles: ['.headline{display:flex;justify-content:space-between;align-items:center;}']
})
export class RunDetailPageComponent {
  private readonly route = inject(ActivatedRoute);
  private readonly dataService = inject(FrontendDataService);

  protected readonly vm$ = this.route.paramMap.pipe(
    switchMap((params) => this.dataService.getRunDetail(params.get('runId') ?? '')),
    map((detail) => ({ detail, error: null as string | null, loading: false })),
    catchError((error: Error) => of({ detail: null, error: error.message, loading: false })),
    startWith({ detail: null, error: null as string | null, loading: true })
  );
}
