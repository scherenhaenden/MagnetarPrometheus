import { Provider } from '@angular/core';
import { environment } from '../../../environments/environment';
import { ApiFrontendDataService } from './api-frontend-data.service';
import { FrontendDataService } from './frontend-data.service';
import { MockFrontendDataService } from './mock-frontend-data.service';

/**
 * Strategy provider for selecting mock or API transport mode.
 */
export const FRONTEND_DATA_SERVICE_PROVIDER: Provider = {
  provide: FrontendDataService,
  useClass: environment.useMockDataService ? MockFrontendDataService : ApiFrontendDataService
};
