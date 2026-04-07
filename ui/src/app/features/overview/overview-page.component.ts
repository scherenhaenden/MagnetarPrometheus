/**
 * Overview page for first web shell.
 * Communicates current product reality and route intent.
 */
import { Component } from '@angular/core';

@Component({
  standalone: true,
  template: `
    <section>
      <h2>Platform Overview</h2>
      <p>This shell is the first browser-visible surface for MagnetarPrometheus.</p>
      <ul>
        <li>Runs: inspect workflow execution history.</li>
        <li>Submit Job: queue a new workflow run (currently mock mode).</li>
        <li>Workflows: discover available workflow templates.</li>
      </ul>
    </section>
  `
})
export class OverviewPageComponent {}
