/**
 * app.config.spec.ts intent header.
 *
 * This test ensures that the application configuration provides
 * the necessary Angular and application-specific providers.
 */
import { appConfig } from './app.config';
import { FRONTEND_DATA_SERVICE_PROVIDER } from './shared/services/frontend-data.provider';

describe('appConfig', () => {
  it('should be defined', () => {
    expect(appConfig).toBeDefined();
  });

  it('should include necessary providers', () => {
    expect(appConfig.providers).toBeDefined();
    // We expect at least the router, http client, and data service providers
    expect(appConfig.providers.length).toBeGreaterThanOrEqual(3);
    expect(appConfig.providers).toContain(FRONTEND_DATA_SERVICE_PROVIDER);
  });
});
