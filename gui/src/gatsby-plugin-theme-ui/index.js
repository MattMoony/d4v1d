import { dark, base } from '@theme-ui/presets';

const theme = {
  ...dark,
  styles: {
    ...dark.styles,
  },
  colors: {
    ...dark.colors,
    background: '#2F3136',
    muted: '#36393f',
    gray: '#202225',
    modes: {
      light: {
        ...base.colors,
        background: '#fff',
        muted: '#f6f6f6',
        gray: '#B9B9B9',
      },
    },
  },
};

export default theme;