/**
 * frontend-data.provider.spec.ts intent header.
 *
 * This test verifies the service provider provides a valid strategy.
 */
import { FRONTEND_DATA_SERVICE_PROVIDER } from './frontend-data.provider';

describe('Frontend Data Provider', () => {
  it('should be defined as a valid provider', () => {
    expect(FRONTEND_DATA_SERVICE_PROVIDER).toBeDefined();
    const provider = FRONTEND_DATA_SERVICE_PROVIDER as any;
    expect(provider.provide).toBeDefined();
    expect(provider.useClass).toBeDefined();
  });
});
