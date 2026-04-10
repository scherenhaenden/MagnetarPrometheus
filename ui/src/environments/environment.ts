/**
 * Production-like environment defaults.
 *
 * In current repo scope we default production builds to API transport mode, while development
 * defaults to mock mode for standalone UI iteration.
 */
export const environment = {
  production: true,
  useMockDataService: false,
  apiBaseUrl: '/api'
};
