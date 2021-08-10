import * as React from 'react';
import { Box, Divider, Flex } from 'theme-ui';
import TitleBar from './TitleBar';

type WindowLayoutProps = {
  children?: React.ReactElement|React.ReactElement[];
};

const WindowLayout = ({ children, }: WindowLayoutProps) => {

  return (
    <Flex sx={{
      width: '100%',
      height: '100%',
      flexDirection: 'column',
      justifyContent: 'stretch',
    }}>
      <TitleBar />
      <Box sx={{
        flexGrow: 1,
      }}>
        {children}
      </Box>
    </Flex>
  );
};

export default WindowLayout;