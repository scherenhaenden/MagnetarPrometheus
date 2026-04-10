/**
 * Electron main process skeleton for MagnetarPrometheus.
 *
 * This desktop host wraps the Angular UI and does not duplicate web-feature logic.
 */
const { app, BrowserWindow } = require('electron');
const path = require('node:path');
const fs = require('node:fs');

const resolveRendererEntry = () => {
  const configuredDistDir = process.env.MP_UI_DIST_DIR;
  const candidateRoots = configuredDistDir
    ? [configuredDistDir]
    : [
        path.resolve(app.getAppPath(), 'ui/dist/magnetar-prometheus-ui/browser'),
        path.resolve(app.getAppPath(), '../ui/dist/magnetar-prometheus-ui/browser'),
        path.resolve(process.resourcesPath, 'ui/dist/magnetar-prometheus-ui/browser'),
        path.resolve(__dirname, '../../ui/dist/magnetar-prometheus-ui/browser')
      ];

  for (const root of candidateRoots) {
    const entry = path.join(root, 'index.html');
    if (fs.existsSync(entry)) {
      return entry;
    }
  }

  throw new Error(
    `Unable to locate Angular renderer bundle. Checked: ${candidateRoots
      .map((root) => path.join(root, 'index.html'))
      .join(', ')}`
  );
};

const createMainWindow = () => {
  const window = new BrowserWindow({
    width: 1280,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true
    }
  });

  const devServerUrl = process.env.MP_UI_DEV_SERVER_URL;
  if (devServerUrl) {
    const parsedUrl = new URL(devServerUrl);
    const isLocalDevUrl =
      !app.isPackaged &&
      ['http:', 'https:'].includes(parsedUrl.protocol) &&
      ['localhost', '127.0.0.1'].includes(parsedUrl.hostname);

    if (!isLocalDevUrl) {
      throw new Error('MP_UI_DEV_SERVER_URL must target a local development server.');
    }

    window.loadURL(devServerUrl);
  } else {
    window.loadFile(resolveRendererEntry());
  }
};

app.whenReady().then(() => {
  createMainWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createMainWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
