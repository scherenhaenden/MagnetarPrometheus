/**
 * overview-page.component.ts intent header.
 *
 * This file is part of the Angular UI slice and exists to keep the
 * route/component/service contract explicit for the current product increment.
 */
import { Component } from '@angular/core';
import { PageContainerComponent } from '../../shared/ui/page-container.component';
import { PageHeaderComponent } from '../../shared/ui/page-header.component';
import { PanelCardComponent } from '../../shared/ui/panel-card.component';

/**
 * OverviewPageComponent serves as the landing or home page for the application.
 *
 * It provides users with a high-level summary of the platform's capabilities
 * and acts as an entry point explaining what features are available within
 * the MagnetarPrometheus UI shell (Run History, Job Submission, Catalog, Environment).
 *
 * This component is currently entirely static and does not require any data fetching logic.
 */
@Component({
  imports: [PageContainerComponent, PageHeaderComponent, PanelCardComponent],
  templateUrl: './overview-page.component.html'
})
export class OverviewPageComponent {}
