/**
 * panel-card.component.ts intent header.
 *
 * This file is part of the Angular UI slice and exists to keep the
 * route/component/service contract explicit for the current product increment.
 */
import { Component } from '@angular/core';

/**
 * PanelCardComponent serves as a foundational UI building block.
 *
 * It provides a consistent visual container (a "card" or "panel") that is used
 * throughout the application to group related content, separate sections visually,
 * and maintain a uniform design language.
 *
 * It acts as a wrapper component, leveraging Angular's content projection
 * (`<ng-content>`) to render whatever HTML or other components are placed inside it.
 */
@Component({
  selector: 'mp-panel-card',
  standalone: true,
  templateUrl: './panel-card.component.html',
  styleUrl: './panel-card.component.css'
})
export class PanelCardComponent {}
