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
    modes: {
      light: {
        ...base.colors,
      },
    },
  },
};

export default theme;