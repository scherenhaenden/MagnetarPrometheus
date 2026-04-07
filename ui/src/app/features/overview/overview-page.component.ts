import { Component } from '@angular/core';
import { PageContainerComponent } from '../../shared/ui/page-container.component';
import { PageHeaderComponent } from '../../shared/ui/page-header.component';
import { PanelCardComponent } from '../../shared/ui/panel-card.component';

@Component({
  standalone: true,
  imports: [PageContainerComponent, PageHeaderComponent, PanelCardComponent],
  template: `
    <mp-page-container>
      <mp-page-header
        title="Platform Overview"
        description="MagnetarPrometheus UI shell for operations, observability, and workflow job dispatch."
      ></mp-page-header>
      <mp-panel-card>
        <ul>
          <li><strong>Run History:</strong> inspect execution lifecycle, filter status, and drill into details.</li>
          <li><strong>Job Submission:</strong> submit new workflow runs using validated input contracts.</li>
          <li><strong>Workflow Catalog:</strong> browse available workflows and metadata summaries.</li>
          <li><strong>Environment:</strong> confirm transport mode and runtime integration assumptions.</li>
        </ul>
      </mp-panel-card>
    </mp-page-container>
  `
})
export class OverviewPageComponent {}
