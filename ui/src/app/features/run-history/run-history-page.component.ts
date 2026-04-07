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

@Component({
  standalone: true,
  imports: [
    AsyncPipe,
    DatePipe,
    NgFor,
    NgIf,
    RouterLink,
    ReactiveFormsModule,
    PageContainerComponent,
    PageHeaderComponent,
    PanelCardComponent,
    DataListWrapperComponent,
    StatusBadgeComponent
  ],
  template: `
    <mp-page-container>
      <mp-page-header
        title="Run History"
        description="Browse recent workflow runs with status filters and keyword search across run/workflow identifiers."
      ></mp-page-header>

      <mp-panel-card>
        <form [formGroup]="filterForm" class="filters">
          <input formControlName="search" placeholder="Search run ID or workflow ID" />
          <select formControlName="status">
            <option value="all">All statuses</option>
            <option value="queued">Queued</option>
            <option value="running">Running</option>
            <option value="succeeded">Succeeded</option>
            <option value="failed">Failed</option>
            <option value="cancelled">Cancelled</option>
          </select>
        </form>
      </mp-panel-card>

      <ng-container *ngIf="vm$ | async as vm">
        <mp-panel-card *ngIf="vm.loading">Loading run history...</mp-panel-card>
        <mp-panel-card *ngIf="vm.error">Unable to load run history: {{ vm.error }}</mp-panel-card>
        <mp-panel-card *ngIf="!vm.loading && !vm.error && vm.items.length === 0">
          No runs match the current filters.
        </mp-panel-card>

        <mp-data-list-wrapper *ngIf="!vm.loading && !vm.error && vm.items.length > 0">
          <mp-panel-card *ngFor="let run of vm.items">
            <div class="run-row">
              <a [routerLink]="['/runs', run.runId]"><strong>{{ run.runId }}</strong></a>
              <mp-status-badge [text]="run.status" [tone]="run.status"></mp-status-badge>
            </div>
            <div>{{ run.workflowId }} · {{ run.createdAtIso | date:'medium' }}</div>
            <div>{{ run.summary }}</div>
          </mp-panel-card>
        </mp-data-list-wrapper>
      </ng-container>
    </mp-page-container>
  `,
  styles: ['.filters{display:grid;grid-template-columns:1fr 220px;gap:var(--mp-space-3);}.run-row{display:flex;justify-content:space-between;align-items:center;}']
})
export class RunHistoryPageComponent {
  private readonly dataService = inject(FrontendDataService);
  private readonly fb = inject(FormBuilder);

  protected readonly filterForm = this.fb.nonNullable.group({
    search: '',
    status: 'all'
  });

  private readonly filterValue$ = this.filterForm.valueChanges.pipe(startWith(this.filterForm.getRawValue()));
  protected readonly vm$ = combineLatest([
    this.dataService.getRunHistory().pipe(
      map((items) => ({ items, error: null as string | null })),
      catchError((error: Error) => of({ items: [], error: error.message }))
    ),
    this.filterValue$
  ]).pipe(
    map(([response, filter]) => {
      const query = (filter.search ?? '').toLowerCase().trim();
      const status = filter.status ?? 'all';
      const filtered = response.items.filter((item) => {
        const searchMatches = query.length === 0 || item.runId.toLowerCase().includes(query) || item.workflowId.toLowerCase().includes(query);
        const statusMatches = status === 'all' || item.status === status;
        return searchMatches && statusMatches;
      });
      return { items: filtered, error: response.error, loading: false };
    }),
    startWith({ items: [], error: null as string | null, loading: true })
  );
}
