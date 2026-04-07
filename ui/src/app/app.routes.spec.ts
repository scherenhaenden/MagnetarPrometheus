import { provideHttpClient } from '@angular/common/http';
import { TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';
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
  });
});
