/**
 * frontend-data.provider.spec.ts intent header.
 *
 * This test verifies the service provider provides a valid strategy.
 */
import { ApiFrontendDataService } from './api-frontend-data.service';
import { MockFrontendDataService } from './mock-frontend-data.service';
import {
  FRONTEND_DATA_SERVICE_PROVIDER,
  selectFrontendDataServiceClass
} from './frontend-data.provider';

describe('Frontend Data Provider', () => {
  it('should be defined as a valid provider', () => {
    expect(FRONTEND_DATA_SERVICE_PROVIDER).toBeDefined();
    const provider = FRONTEND_DATA_SERVICE_PROVIDER as any;
    expect(provider.provide).toBeDefined();
    expect(provider.useClass).toBeDefined();
  });

  it('should select the mock adapter when mock transport is enabled', () => {
    expect(selectFrontendDataServiceClass(true)).toBe(MockFrontendDataService);
  });

  it('should select the API adapter when mock transport is disabled', () => {
    expect(selectFrontendDataServiceClass(false)).toBe(ApiFrontendDataService);
  });
});
