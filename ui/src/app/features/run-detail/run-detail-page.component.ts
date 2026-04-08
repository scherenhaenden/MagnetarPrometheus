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

@Component({
    imports: [AsyncPipe, DatePipe, RouterLink, PageContainerComponent, PageHeaderComponent, PanelCardComponent, StatusBadgeComponent],
    template: `
    <mp-page-container>
      <mp-page-header
        title="Run Detail"
        description="Inspect selected run metadata, step timeline, and execution output preview."
      ></mp-page-header>

      @if (vm$ | async; as vm) {
        @if (vm.loading) {
          <mp-panel-card>Loading run detail...</mp-panel-card>
        }
        @if (vm.error) {
          <mp-panel-card>Unable to load run detail: {{ vm.error }}</mp-panel-card>
        }
        @if (!vm.loading && !vm.error && !vm.detail) {
          <mp-panel-card>No run found for the selected identifier.</mp-panel-card>
        }
        @if (!vm.loading && !vm.error && vm.detail; as detail) {
          <mp-panel-card>
            <div class="headline"><strong>{{ detail.runId }}</strong><mp-status-badge [text]="detail.status" [tone]="detail.status"></mp-status-badge></div>
            <p>Workflow: {{ detail.workflowId }}</p>
            <p>Created: {{ detail.createdAtIso | date:'medium' }}</p>
            @if (detail.completedAtIso) {
              <p>Completed: {{ detail.completedAtIso | date:'medium' }}</p>
            }
            @if (detail.errorMessage) {
              <p>Error: {{ detail.errorMessage }}</p>
            }
            <p>Output preview: {{ detail.outputPreview }}</p>
          </mp-panel-card>
          <mp-panel-card>
            <h3>Step Timeline</h3>
            <ul>
              @for (step of detail.steps; track step) {
                <li>
                  <strong>{{ step.name }}</strong> — {{ step.state }} — {{ step.detail }}
                </li>
              }
            </ul>
            <a routerLink="/runs">Back to run history</a>
          </mp-panel-card>
        }
      }
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
