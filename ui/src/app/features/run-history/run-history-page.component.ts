/**
 * Run history feature slice.
 */
import { AsyncPipe, DatePipe, NgFor } from '@angular/common';
import { Component, inject } from '@angular/core';
import { RouterLink } from '@angular/router';
import { FrontendDataService } from '../../shared/services/frontend-data.service';

@Component({
  standalone: true,
  imports: [AsyncPipe, RouterLink, DatePipe, NgFor],
  template: `
    <section>
      <h2>Run History</h2>
      <p>Current mode uses the frontend mock adapter until API endpoints land.</p>
      <div *ngFor="let run of (runs$ | async)" class="run-card">
        <a [routerLink]="['/runs', run.runId]"><strong>{{ run.runId }}</strong></a>
        <div>{{ run.workflowId }} · {{ run.status }}</div>
        <div>Created: {{ run.createdAtIso | date:'medium' }}</div>
        <div>{{ run.summary }}</div>
      </div>
    </section>
  `,
  styles: ['.run-card{border:1px solid #264261; border-radius:.5rem; padding:.75rem; margin:.5rem 0; background:#101b2c;}']
})
export class RunHistoryPageComponent {
  private readonly dataService = inject(FrontendDataService);
  protected readonly runs$ = this.dataService.getRunHistory();
}
