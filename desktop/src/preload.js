/**
 * Secure bridge placeholder.
 *
 * The preload layer is intentionally minimal until explicit desktop-only IPC requirements
 * are approved. Frontend should remain web-first and transport-agnostic.
 */
const { contextBridge } = require('electron');

contextBridge.exposeInMainWorld('magnetarDesktop', {
  platform: process.platform,
  version: process.versions.electron,
  ping: () => 'pong'
});
