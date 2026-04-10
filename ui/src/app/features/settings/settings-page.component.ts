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

/**
 * SettingsPageComponent provides a view into the application's current environment and transport configuration.
 *
 * It is primarily used for operational visibility, allowing the user to confirm whether the UI
 * is running in 'mock' mode or 'api' mode, and to inspect the underlying base URL used for requests.
 */
@Component({
  imports: [PageContainerComponent, PageHeaderComponent, PanelCardComponent],
  templateUrl: './settings-page.component.html'
})
export class SettingsPageComponent {
  /**
   * Provides the template access to the globally configured environment variables.
   */
  protected readonly environment = environment;
}
