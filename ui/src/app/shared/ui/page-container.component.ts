/**
 * page-container.component.ts intent header.
 *
 * This file is part of the Angular UI slice and exists to keep the
 * route/component/service contract explicit for the current product increment.
 */
import { Component } from '@angular/core';

/**
 * PageContainerComponent provides the structural foundation for top-level feature views.
 *
 * It acts as a primary layout wrapper, ensuring consistent horizontal constraints (max-width),
 * centering, and vertical rhythm (gap spacing) across all distinct pages within the application shell.
 * It is meant to be the outermost element used within the template of a routed feature component.
 */
@Component({
  selector: 'mp-page-container',
  standalone: true,
  templateUrl: './page-container.component.html',
  styleUrl: './page-container.component.css'
})
export class PageContainerComponent {}
