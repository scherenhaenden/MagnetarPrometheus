/**
 * app.config.ts intent header.
 *
 * This file is part of the Angular UI slice and exists to keep the
 * route/component/service contract explicit for the current product increment.
 */
import { ApplicationConfig } from '@angular/core';
import { provideHttpClient } from '@angular/common/http';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import { FRONTEND_DATA_SERVICE_PROVIDER } from './shared/services/frontend-data.provider';

export const appConfig: ApplicationConfig = {
  providers: [provideRouter(routes), provideHttpClient(), FRONTEND_DATA_SERVICE_PROVIDER]
};
