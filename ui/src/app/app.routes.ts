/**
 * Top-level route map for the MagnetarPrometheus web shell.
 *
 * The route map intentionally separates product slices so each feature packet can evolve
 * independently with disjoint ownership.
 */
import { Routes } from '@angular/router';
import { AppShellComponent } from './core/layout/app-shell.component';
import { JobSubmissionPageComponent } from './features/job-submission/job-submission-page.component';
import { OverviewPageComponent } from './features/overview/overview-page.component';
import { RunDetailPageComponent } from './features/run-detail/run-detail-page.component';
import { RunHistoryPageComponent } from './features/run-history/run-history-page.component';
import { SettingsPageComponent } from './features/settings/settings-page.component';
import { WorkflowCatalogPageComponent } from './features/workflow-catalog/workflow-catalog-page.component';

export const routes: Routes = [
  {
    path: '',
    component: AppShellComponent,
    children: [
      { path: '', component: OverviewPageComponent },
      { path: 'runs', component: RunHistoryPageComponent },
      { path: 'runs/:runId', component: RunDetailPageComponent },
      { path: 'submit', component: JobSubmissionPageComponent },
      { path: 'workflows', component: WorkflowCatalogPageComponent },
      { path: 'settings', component: SettingsPageComponent }
    ]
  }
];
