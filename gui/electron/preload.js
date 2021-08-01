const { contextBridge, ipcRenderer, remote } = require('electron');

contextBridge.exposeInMainWorld(
  'api', {
    send: (channel, ...data) => {
      const validChannels = ['toMain',];
      if (validChannels.includes(channel)) ipcRenderer.send(channel, ...data);
    },
    receive: (channel, func) => {
      const validChannels = ['fromMain',];
      if (validChannels.includes(channel)) ipcRenderer.on(channel, (e, ...args) => func(...args));
    },
  }
);