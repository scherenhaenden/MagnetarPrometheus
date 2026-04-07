/**
 * Run detail page for selected run id.
 */
import { AsyncPipe, NgFor, NgIf } from '@angular/common';
import { Component, inject } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { switchMap } from 'rxjs';
import { FrontendDataService } from '../../shared/services/frontend-data.service';

@Component({
  standalone: true,
  imports: [AsyncPipe, NgFor, NgIf],
  template: `
    <section>
      <h2>Run Detail</h2>
      <ng-container *ngIf="detail$ | async as detail; else missing">
        <p><strong>{{ detail.runId }}</strong> · {{ detail.status }}</p>
        <p>{{ detail.outputPreview }}</p>
        <ul>
          <li *ngFor="let step of detail.steps">{{ step.name }} — {{ step.state }}</li>
        </ul>
      </ng-container>
      <ng-template #missing>
        <p>Run not found in the current adapter.</p>
      </ng-template>
    </section>
  `
})
export class RunDetailPageComponent {
  private readonly route = inject(ActivatedRoute);
  private readonly dataService = inject(FrontendDataService);
  protected readonly detail$ = this.route.paramMap.pipe(
    switchMap((params) => this.dataService.getRunDetail(params.get('runId') ?? ''))
  );
}
