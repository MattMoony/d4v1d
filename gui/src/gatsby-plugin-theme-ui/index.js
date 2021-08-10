import { dark, base } from '@theme-ui/presets';

const theme = {
  ...dark,
  styles: {
    ...dark.styles,
  },
  fonts: {
    ...dark.fonts,
    monospace: 'Fira Code, Menlo, monospace',
  },
  colors: {
    ...dark.colors,
    background: '#2F3136',
    muted: '#36393f',
    gray: '#202225',
    lightGray: '#b9bbbe',
    modes: {
      light: {
        ...base.colors,
        background: '#fff',
        muted: '#f6f6f6',
        gray: '#B9B9B9',
        lightGray: '#171718',
      },
    },
  },
};

export default theme;