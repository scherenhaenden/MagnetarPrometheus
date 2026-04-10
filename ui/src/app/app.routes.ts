/**
 * Top-level route map for the MagnetarPrometheus web shell.
 *
 * The route map intentionally separates product slices so each feature packet can evolve
 * independently with disjoint ownership.
 */
import { Routes } from '@angular/router';
import { AppShellComponent } from './core/layout/app-shell.component';

export const routes: Routes = [
  {
    path: '',
    component: AppShellComponent,
    children: [
      {
        path: '',
        loadComponent: () =>
          import('./features/overview/overview-page.component').then((m) => m.OverviewPageComponent)
      },
      {
        path: 'runs',
        loadComponent: () =>
          import('./features/run-history/run-history-page.component').then((m) => m.RunHistoryPageComponent)
      },
      {
        path: 'runs/:runId',
        loadComponent: () =>
          import('./features/run-detail/run-detail-page.component').then((m) => m.RunDetailPageComponent)
      },
      {
        path: 'submit',
        loadComponent: () =>
          import('./features/job-submission/job-submission-page.component').then((m) => m.JobSubmissionPageComponent)
      },
      {
        path: 'workflows',
        loadComponent: () =>
          import('./features/workflow-catalog/workflow-catalog-page.component').then((m) => m.WorkflowCatalogPageComponent)
      },
      {
        path: 'studio',
        loadComponent: () =>
          import('./features/workflow-studio/workflow-studio-page.component').then((m) => m.WorkflowStudioPageComponent)
      },
      {
        path: 'settings',
        loadComponent: () =>
          import('./features/settings/settings-page.component').then((m) => m.SettingsPageComponent)
      },
      { path: '**', redirectTo: '' }
    ]
  }
];
