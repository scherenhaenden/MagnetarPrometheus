/**
 * Workflow Studio page.
 *
 * This component introduces the first user-visible slice of the visual workflow builder.
 * The layout intentionally reflects the target architecture with five regions:
 * library, canvas, inspector, toolbar, and diagnostics.
 *
 * This increment also ships persisted example workflows (YAML/JSON/TOML) so operators can
 * immediately inspect a concrete flow in the UI while the visual editor remains in progress.
 */
import { HttpClient } from '@angular/common/http';
import { Component, inject } from '@angular/core';

interface WorkflowExampleAsset {
  readonly format: 'yaml' | 'json' | 'toml';
  readonly label: string;
  readonly path: string;
}

@Component({
  selector: 'app-workflow-studio-page',
  standalone: true,
  templateUrl: './workflow-studio-page.component.html',
  styleUrl: './workflow-studio-page.component.css'
})
export class WorkflowStudioPageComponent {
  private readonly http = inject(HttpClient);

  protected readonly examples: ReadonlyArray<WorkflowExampleAsset> = [
    { format: 'yaml', label: 'YAML', path: '/assets/workflows/examples/support-ticket-triage.yaml' },
    { format: 'json', label: 'JSON', path: '/assets/workflows/examples/support-ticket-triage.json' },
    { format: 'toml', label: 'TOML', path: '/assets/workflows/examples/support-ticket-triage.toml' }
  ];

  protected selectedExample: WorkflowExampleAsset = this.examples[0];
  protected exampleContent = '';
  protected loadingExample = true;
  protected exampleError: string | null = null;

  constructor() {
    this.loadExample(this.selectedExample);
  }

  protected selectExample(example: WorkflowExampleAsset): void {
    this.selectedExample = example;
    this.loadExample(example);
  }

  private loadExample(example: WorkflowExampleAsset): void {
    this.loadingExample = true;
    this.exampleError = null;

    this.http.get(example.path, { responseType: 'text' }).subscribe({
      next: (content) => {
        this.exampleContent = content;
        this.loadingExample = false;
      },
      error: () => {
        this.exampleContent = '';
        this.exampleError = `Unable to load ${example.label} workflow example from ${example.path}.`;
        this.loadingExample = false;
      }
    });
  }
}
