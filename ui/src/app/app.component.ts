/**
 * Root application component.
 *
 * This component intentionally delegates all visible structure to the routed shell.
 * Keeping this file thin helps avoid centralizing feature concerns in one monolith.
 */
import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
    selector: 'app-root',
    imports: [RouterOutlet],
    templateUrl: './app.component.html',
    styleUrl: './app.component.css'
})
export class AppComponent {}
