/**
 * Workflow Studio page.
 *
 * This component introduces the first user-visible slice of the visual workflow builder.
 * The layout intentionally reflects the target architecture with five regions:
 * library, canvas, inspector, toolbar, and diagnostics.
 *
 * For this first increment, regions are non-interactive placeholders so the route and
 * product framing can be validated before wiring graph state and runtime integrations.
 */
import { Component } from '@angular/core';

@Component({
  selector: 'app-workflow-studio-page',
  templateUrl: './workflow-studio-page.component.html',
  styleUrl: './workflow-studio-page.component.css'
})
export class WorkflowStudioPageComponent {}
