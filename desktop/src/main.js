/**
 * Electron main process skeleton for MagnetarPrometheus.
 *
 * This desktop host wraps the Angular UI and does not duplicate web-feature logic.
 */
const { app, BrowserWindow } = require('electron');
const path = require('node:path');

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
    window.loadURL(devServerUrl);
  } else {
    window.loadFile(path.resolve(__dirname, '../../ui/dist/magnetar-prometheus-ui/browser/index.html'));
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
