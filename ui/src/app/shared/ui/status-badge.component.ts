/**
 * status-badge.component.ts intent header.
 *
 * This file is part of the Angular UI slice and exists to keep the
 * route/component/service contract explicit for the current product increment.
 */
import { NgClass } from '@angular/common';
import { Component, Input } from '@angular/core';

@Component({
  selector: 'mp-status-badge',
  standalone: true,
  imports: [NgClass],
  template: '<span class="badge" [ngClass]="tone">{{ text }}</span>',
  styles: [
    '.badge{display:inline-flex;padding:var(--mp-space-1) var(--mp-space-2);border-radius:999px;border:1px solid;font-size:.75rem;text-transform:capitalize;font-weight:600;}',
    '.healthy,.succeeded,.done{background:#143d2e;border-color:#2b8a5d;color:#c8f0de;}',
    '.degraded,.queued,.running,.pending{background:#3c330f;border-color:#b98b24;color:#ffe7a4;}',
    '.offline,.failed,.cancelled{background:#4b1f1f;border-color:#bd4848;color:#ffd3d3;}'
  ]
})
export class StatusBadgeComponent {
  @Input({ required: true }) text = '';
  @Input() tone = '';
}
