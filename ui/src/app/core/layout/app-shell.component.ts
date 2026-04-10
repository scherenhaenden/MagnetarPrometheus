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
import { catchError, map, of, shareReplay, startWith } from 'rxjs';
import { FrontendDataService } from '../../shared/services/frontend-data.service';

/**
 * AppShellComponent acts as the main layout container for the entire application.
 *
 * It is responsible for setting up the overarching DOM structure which includes:
 * - A top bar containing the application title, description, and dynamic service health status.
 * - A side navigation bar containing links to primary feature areas.
 * - A main content area utilizing a router-outlet to dynamically load feature components based on the active route.
 *
 * The component relies on the `FrontendDataService` to proactively poll or retrieve service health information,
 * transforming this data into observable streams (`healthTone$` and `healthLabel$`) that update the UI reactively.
 * This ensures the user is always aware of the system's operational status and current transport mode (API vs Mock).
 */
@Component({
  selector: 'app-shell',
  imports: [RouterOutlet, RouterLink, RouterLinkActive, AsyncPipe, NgClass],
  templateUrl: './app-shell.component.html',
  styleUrl: './app-shell.component.css'
})
export class AppShellComponent {
  /**
   * Injects the `FrontendDataService` which provides access to platform status and workflows.
   * We use the `inject` function for dependency injection, a more modern Angular approach
   * compared to constructor injection, promoting cleaner class definitions.
   */
  private readonly dataService = inject(FrontendDataService);

  /**
   * Observable stream representing the continuous health status of the backend service.
   *
   * How it works:
   * 1. It initiates a request to `getServiceHealth()` on the `FrontendDataService`.
   * 2. `catchError` is utilized to intercept any network or service-level failures. In such cases,
   *    it gracefully degrades by returning a fallback snapshot indicating an 'offline' status.
   * 3. `shareReplay({ bufferSize: 1, refCount: true })` ensures that multiple subscriptions
   *    (e.g., from `healthTone$` and `healthLabel$`) do not trigger multiple underlying HTTP requests.
   *    It caches the latest health snapshot and shares it.
   */
  protected readonly health$ = this.dataService.getServiceHealth().pipe(
    catchError(() =>
      of({
        status: 'offline' as const,
        message: 'Service unreachable',
        checkedAtIso: new Date().toISOString(),
        mode: 'api' as const
      })
    ),
    shareReplay({ bufferSize: 1, refCount: true })
  );

  /**
   * Observable stream derived from `health$`, specifically targeting the status tone (color/styling).
   *
   * It maps the complex health object to just its status string (e.g., 'healthy', 'degraded', 'offline').
   * `startWith('degraded')` provides an immediate initial value before the first network response arrives,
   * ensuring the UI has a safe default class to apply via `[ngClass]`.
   */
  protected readonly healthTone$ = this.health$.pipe(
    map((snapshot) => snapshot.status),
    startWith('degraded')
  );

  /**
   * Observable stream derived from `health$`, generating a human-readable status label.
   *
   * It constructs a descriptive string combining status, current transport mode (uppercase), and a detailed message.
   * `startWith('Loading service health...')` provides immediate textual feedback in the UI while
   * the initial health check is in progress.
   */
  protected readonly healthLabel$ = this.health$.pipe(
    map((snapshot) => `${snapshot.status} · ${snapshot.mode.toUpperCase()} · ${snapshot.message}`),
    startWith('Loading service health...')
  );
}
