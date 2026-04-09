/**
 * data-list-wrapper.component.ts intent header.
 *
 * This file is part of the Angular UI slice and exists to keep the
 * route/component/service contract explicit for the current product increment.
 */
import { Component } from '@angular/core';

/**
 * DataListWrapperComponent functions as a structural helper for presenting lists of data items.
 *
 * It is primarily intended to wrap collections of `mp-panel-card` components
 * (often rendered within an `@for` loop). It establishes a consistent vertical flow
 * and standardized spacing (gap) between the rendered items in the list, ensuring
 * that data grids across different features maintain a uniform appearance.
 */
@Component({
  selector: 'mp-data-list-wrapper',
  standalone: true,
  templateUrl: './data-list-wrapper.component.html',
  styleUrl: './data-list-wrapper.component.css'
})
export class DataListWrapperComponent {}
