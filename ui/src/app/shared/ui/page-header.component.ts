import { Component, Input } from '@angular/core';

@Component({
  selector: 'mp-page-header',
  standalone: true,
  template: `
    <header class="page-header">
      <h2>{{ title }}</h2>
      <p>{{ description }}</p>
      <ng-content></ng-content>
    </header>
  `,
  styles: [
    '.page-header h2{margin:0;font-size:1.5rem;}',
    '.page-header p{margin:var(--mp-space-1) 0 0;color:var(--mp-color-text-muted);}'
  ]
})
export class PageHeaderComponent {
  @Input({ required: true }) title = '';
  @Input({ required: true }) description = '';
}
