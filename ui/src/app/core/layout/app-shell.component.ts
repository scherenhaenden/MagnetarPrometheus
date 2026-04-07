/**
 * App shell layout component.
 *
 * Responsibilities:
 * - Provide a coherent frame (header, navigation, content region) for every route.
 * - Host the service health indicator in one shared place.
 * - Avoid feature-specific business behavior; feature routes render within router outlet.
 */
import { AsyncPipe, NgClass } from '@angular/common';
import { Component, inject } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { FrontendDataService } from '../../shared/services/frontend-data.service';

@Component({
  selector: 'app-shell',
  standalone: true,
  imports: [RouterOutlet, RouterLink, RouterLinkActive, AsyncPipe, NgClass],
  template: `
    <div class="shell">
      <header class="topbar">
        <div>
          <h1>MagnetarPrometheus</h1>
          <p>Workflow orchestration control surface (Angular shell increment).</p>
        </div>
        <div class="status" [ngClass]="(health$ | async)?.status">
          {{ (health$ | async)?.status ?? 'checking' }} · {{ (health$ | async)?.mode ?? '...' }}
        </div>
      </header>

      <div class="body">
        <nav class="sidenav">
          <a routerLink="/" [routerLinkActive]="'active'" [routerLinkActiveOptions]="{ exact: true }">Overview</a>
          <a routerLink="/runs" routerLinkActive="active">Runs</a>
          <a routerLink="/submit" routerLinkActive="active">Submit Job</a>
          <a routerLink="/workflows" routerLinkActive="active">Workflows</a>
          <a routerLink="/settings" routerLinkActive="active">Settings</a>
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
}
