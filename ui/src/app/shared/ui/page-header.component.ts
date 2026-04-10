/**
 * page-header.component.ts intent header.
 *
 * This file is part of the Angular UI slice and exists to keep the
 * route/component/service contract explicit for the current product increment.
 */
import { Component, Input } from '@angular/core';

/**
 * PageHeaderComponent creates a standardized, consistent title area for feature views.
 *
 * It ensures that every distinct page begins with a clear, stylistically uniform heading (H2)
 * and a brief, muted descriptive paragraph explaining the purpose of the view.
 * It also supports content projection, allowing developers to inject context-specific
 * action buttons or controls directly into the header area alongside the title.
 */
@Component({
  selector: 'mp-page-header',
  standalone: true,
  templateUrl: './page-header.component.html',
  styleUrl: './page-header.component.css'
})
export class PageHeaderComponent {
  /**
   * The primary title string displayed prominently at the top of the header.
   * Marked as required to enforce consistency across pages.
   */
  @Input({ required: true }) public title = '';

  /**
   * A secondary, muted string that elaborates on the purpose of the page,
   * displayed directly beneath the title. Marked as required to enforce consistency.
   */
  @Input({ required: true }) public description = '';
}
