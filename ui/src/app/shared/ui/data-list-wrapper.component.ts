/**
 * data-list-wrapper.component.ts intent header.
 *
 * This file is part of the Angular UI slice and exists to keep the
 * route/component/service contract explicit for the current product increment.
 */
import { Component } from '@angular/core';

@Component({
  selector: 'mp-data-list-wrapper',
  standalone: true,
  template: '<div class="list"><ng-content></ng-content></div>',
  styles: ['.list{display:flex;flex-direction:column;gap:var(--mp-space-3);}']
})
export class DataListWrapperComponent {}
