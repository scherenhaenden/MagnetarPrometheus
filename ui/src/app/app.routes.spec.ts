/**
 * app.routes.spec.ts intent header.
 *
 * This file is part of the Angular UI slice and exists to keep the
 * route/component/service contract explicit for the current product increment.
 */
import { provideHttpClient } from '@angular/common/http';
import { TestBed } from '@angular/core/testing';
import { Route, Router } from '@angular/router';
import { provideRouter } from '@angular/router';
import { AppComponent } from './app.component';
import { routes } from './app.routes';
import { FrontendDataService } from './shared/services/frontend-data.service';
import { MockFrontendDataService } from './shared/services/mock-frontend-data.service';

describe('App routes smoke', () => {
  let router: Router;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AppComponent],
      providers: [
        provideRouter(routes),
        provideHttpClient(),
        { provide: FrontendDataService, useClass: MockFrontendDataService }
      ]
    }).compileComponents();

    router = TestBed.inject(Router);
  });

  it('contains required top-level feature routes', async () => {
    await router.navigateByUrl('/runs');
    expect(router.url).toBe('/runs');

    await router.navigateByUrl('/submit');
    expect(router.url).toBe('/submit');

    await router.navigateByUrl('/workflows');
    expect(router.url).toBe('/workflows');

    await router.navigateByUrl('/studio');
    expect(router.url).toBe('/studio');
  });

  it('lazy-loads the overview, run detail, and settings components', async () => {
    const childRoutes = (routes[0] as Route).children ?? [];

    const overviewRoute = childRoutes.find((route) => route.path === '');
    const runDetailRoute = childRoutes.find((route) => route.path === 'runs/:runId');
    const settingsRoute = childRoutes.find((route) => route.path === 'settings');

    await expectAsync((overviewRoute?.loadComponent as () => Promise<unknown>)()).toBeResolved();
    await expectAsync((runDetailRoute?.loadComponent as () => Promise<unknown>)()).toBeResolved();
    await expectAsync((settingsRoute?.loadComponent as () => Promise<unknown>)()).toBeResolved();
  });
});
