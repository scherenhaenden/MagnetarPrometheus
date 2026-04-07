import { Component } from '@angular/core';

@Component({
  selector: 'mp-data-list-wrapper',
  standalone: true,
  template: '<div class="list"><ng-content></ng-content></div>',
  styles: ['.list{display:flex;flex-direction:column;gap:var(--mp-space-3);}']
})
export class DataListWrapperComponent {}
