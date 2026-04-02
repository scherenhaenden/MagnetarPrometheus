/**
 * Intent:
 * This is the root application shell component for MagnetarPrometheus.
 * It provides the top-level container for the routing outlet where the actual
 * application features (like Run History or Job Submission) will be rendered.
 *
 * Constraints:
 * - This file must not implement business logic directly.
 * - It should only serve as the visual layout orchestrator for the top-level app frame.
 * - The workspace is strictly Angular.
 */
import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'magnetar-prometheus-ui';
}
