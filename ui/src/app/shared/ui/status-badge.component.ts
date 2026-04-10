/**
 * status-badge.component.ts intent header.
 *
 * This file is part of the Angular UI slice and exists to keep the
 * route/component/service contract explicit for the current product increment.
 */
import { NgClass } from '@angular/common';
import { Component, Input } from '@angular/core';

/**
 * StatusBadgeComponent is a highly reusable UI element designed to visually
 * represent the state or health of a given entity (e.g., a workflow run, the backend service).
 *
 * It uses semantic color-coding (tones) to quickly convey status at a glance
 * (e.g., green for healthy/success, yellow for pending/degraded, red for failure/offline).
 */
@Component({
  selector: 'mp-status-badge',
  imports: [NgClass],
  templateUrl: './status-badge.component.html',
  styleUrl: './status-badge.component.css'
})
export class StatusBadgeComponent {
  /**
   * The text content to display inside the badge.
   * This is typically the exact status string returned from the backend.
   * This input is required to ensure the badge always has content to display.
   */
  @Input({ required: true }) public text = '';

  /**
   * The 'tone' dictates the visual styling (colors) applied to the badge.
   * It maps directly to CSS classes defined in the component's stylesheet.
   * By passing the status string as the tone, the `[ngClass]` binding in the template
   * dynamically applies the correct color scheme based on predefined status groups
   * (e.g., 'succeeded' gets green styles, 'failed' gets red styles).
   */
  @Input() public tone = '';
}
