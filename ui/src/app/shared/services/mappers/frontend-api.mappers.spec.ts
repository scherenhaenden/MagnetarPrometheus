/**
 * frontend-api.mappers.spec.ts intent header.
 *
 * This test file validates mapping functions in frontend-api.mappers.
 */
import { mapHealthApiResponseToSnapshot } from './frontend-api.mappers';

describe('Frontend API Mappers', () => {
  describe('mapHealthApiResponseToSnapshot', () => {
    it('should map correctly', () => {
      const response = {
        status: 'healthy' as const,
        message: 'All good',
        checked_at: '2026-01-01T00:00:00Z'
      };

      const snapshot = mapHealthApiResponseToSnapshot(response, 'api');

      expect(snapshot.status).toBe('healthy');
      expect(snapshot.message).toBe('All good');
      expect(snapshot.checkedAtIso).toBe('2026-01-01T00:00:00Z');
      expect(snapshot.mode).toBe('api');
    });
  });
});
