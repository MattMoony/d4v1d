import { app, BrowserWindow, ipcMain } from "electron";
import { IpcMainEvent } from "electron/main";
import * as path from 'path';

let win: BrowserWindow;

declare global {
  interface Window { 
    api: {
      send: (channel: string, data: any) => void;
      receive: (channel: string, func: (...args: any[]) => void) => void;
    };
  }
}

function createWindow(): void {
  win = new BrowserWindow({
    width: 800,
    height: 600,
    minWidth: 700,
    minHeight: 500,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      enableRemoteModule: false,
      preload: path.resolve(__dirname, 'preload.js'),
    },
    show: false,
    frame: false,
    resizable: true,
    backgroundColor: '#060606',
    title: 'd4v1d',
  });

  process.env['ELECTRON_DISABLE_SECURITY_WARNINGS'] = 'true';
  win.webContents.openDevTools();

  ipcMain.on('toMain', (e: IpcMainEvent, action: string, ...args: any[]) => {
    switch (action) {
      case 'minimize':
        win.minimize();
        break;
      case 'maximize':
        if (win.isMaximized()) win.unmaximize();
        else win.maximize();
        break;
      case 'close':
        win.close();
        break;
    }
  });

  win.loadURL('http://localhost:8000/');
  win.once('ready-to-show', () => win.show());

}

app.on('ready', createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

app.on('activate', () => {
  if (win === null) createWindow();
});