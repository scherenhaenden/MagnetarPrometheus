import { Component } from '@angular/core';

@Component({
  selector: 'mp-page-container',
  standalone: true,
  template: '<section class="page-container"><ng-content></ng-content></section>',
  styles: [
    '.page-container{display:flex;flex-direction:column;gap:var(--mp-space-4);max-width:1200px;margin:0 auto;width:100%;}'
  ]
})
export class PageContainerComponent {}
