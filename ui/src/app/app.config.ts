import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import { FrontendDataService } from './shared/services/frontend-data.service';
import { MockFrontendDataService } from './shared/services/mock-frontend-data.service';

export const appConfig: ApplicationConfig = {
  providers: [provideRouter(routes), { provide: FrontendDataService, useClass: MockFrontendDataService }]
};
