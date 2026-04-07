/**
 * App shell layout component.
 *
 * Responsibilities:
 * - Provide a cohesive desktop-oriented frame with responsive fallback behavior.
 * - Host global navigation and transport-mode-aware health indication.
 * - Keep feature routes isolated in router-outlet.
 */
import { AsyncPipe, NgClass } from '@angular/common';
import { Component, inject } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { map, startWith } from 'rxjs';
import { FrontendDataService } from '../../shared/services/frontend-data.service';

@Component({
  selector: 'app-shell',
  standalone: true,
  imports: [RouterOutlet, RouterLink, RouterLinkActive, AsyncPipe, NgClass],
  template: `
    <div class="shell">
      <header class="topbar">
        <div>
          <h1>MagnetarPrometheus Control Surface</h1>
          <p>Operational UI for workflow history, job submission, and workflow catalog management.</p>
        </div>
        <div class="status" [ngClass]="(healthTone$ | async) ?? 'degraded'">
          {{ (healthLabel$ | async) ?? 'Checking service status...' }}
        </div>
      </header>

      <div class="body">
        <nav class="sidenav">
          <a routerLink="/" [routerLinkActive]="'active'" [routerLinkActiveOptions]="{ exact: true }">Overview</a>
          <a routerLink="/runs" routerLinkActive="active">Run History</a>
          <a routerLink="/submit" routerLinkActive="active">Job Submission</a>
          <a routerLink="/workflows" routerLinkActive="active">Workflow Catalog</a>
          <a routerLink="/settings" routerLinkActive="active">Environment</a>
        </nav>

        <main class="content">
          <router-outlet></router-outlet>
        </main>
      </div>
    </div>
  `,
  styleUrl: './app-shell.component.css'
})
export class AppShellComponent {
  private readonly dataService = inject(FrontendDataService);
  protected readonly health$ = this.dataService.getServiceHealth();
  protected readonly healthTone$ = this.health$.pipe(map((snapshot) => snapshot.status), startWith('degraded'));
  protected readonly healthLabel$ = this.health$.pipe(
    map((snapshot) => `${snapshot.status} · ${snapshot.mode.toUpperCase()} · ${snapshot.message}`),
    startWith('Loading service health...')
  );
}
