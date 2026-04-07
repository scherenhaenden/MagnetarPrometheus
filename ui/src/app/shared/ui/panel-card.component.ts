import { Component } from '@angular/core';

@Component({
  selector: 'mp-panel-card',
  standalone: true,
  template: '<article class="panel"><ng-content></ng-content></article>',
  styles: [
    '.panel{background:var(--mp-color-surface-raised);border:1px solid var(--mp-color-border);border-radius:var(--mp-radius-lg);padding:var(--mp-space-4);box-shadow:var(--mp-elevation-1);}'
  ]
})
export class PanelCardComponent {}
