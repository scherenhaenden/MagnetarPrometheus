/**
 * settings-page.component.ts intent header.
 *
 * This file is part of the Angular UI slice and exists to keep the
 * route/component/service contract explicit for the current product increment.
 */
import { Component } from '@angular/core';
import { environment } from '../../../environments/environment';
import { PageContainerComponent } from '../../shared/ui/page-container.component';
import { PageHeaderComponent } from '../../shared/ui/page-header.component';
import { PanelCardComponent } from '../../shared/ui/panel-card.component';

@Component({
    imports: [PageContainerComponent, PageHeaderComponent, PanelCardComponent],
    template: `
    <mp-page-container>
      <mp-page-header title="Environment Settings" description="Runtime-mode visibility for frontend transport strategy."></mp-page-header>
      <mp-panel-card>
        <p>Transport mode: <strong>{{ environment.useMockDataService ? 'mock' : 'api' }}</strong></p>
        <p>API base URL: <code>{{ environment.apiBaseUrl }}</code></p>
      </mp-panel-card>
    </mp-page-container>
  `
})
export class SettingsPageComponent {
  protected readonly environment = environment;
}
