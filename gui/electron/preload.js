const { contextBridge, ipcRenderer, remote } = require('electron');

const listeners = {};

contextBridge.exposeInMainWorld(
  'api', {
    send: (channel, ...data) => {
      const validChannels = ['toMain',];
      if (validChannels.includes(channel)) ipcRenderer.send(channel, ...data);
    },
    receive: (channel, action, func) => {
      const validChannels = ['fromMain',];
      if (validChannels.includes(channel)) {
        if (listeners[action]) ipcRenderer.removeListener(channel, listeners[action]);
        listeners[action] = (...args) => func(...args);
        ipcRenderer.on(channel, (e, _action, ..._args) => {
          if (_action === action) listeners[action](..._args);
        });
      }
    },
  }
);