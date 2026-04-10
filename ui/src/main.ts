import { provideZoneChangeDetection } from "@angular/core";
/**
 * Intent:
 * This file serves as the main entrypoint for the MagnetarPrometheus Angular web UI.
 * It bootstraps the root `AppComponent` using the standalone component architecture
 * introduced in modern Angular. This file orchestrates the initial application load
 * but does not contain business logic.
 *
 * Architecture Constraint:
 * The frontend surface remains Angular-only. Any future initialization hooks (like
 * environment-specific config loading or SDK initialization) should be wired into
 * `appConfig` rather than accumulating in this raw entrypoint file.
 */
import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { AppComponent } from './app/app.component';

bootstrapApplication(AppComponent, {...appConfig, providers: [provideZoneChangeDetection(), ...appConfig.providers]})
  .catch((err) => console.error(err));
