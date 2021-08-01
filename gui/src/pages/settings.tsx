import * as React from 'react';
import { Box, Close, Divider, Flex, Heading, IconButton, useColorMode } from "theme-ui";
import WindowLayout from '../components/WindowLayout';
import { Link } from 'gatsby';
import Setting from '../components/Setting';

const Settings = () => {
  const [colorMode, setMode] = useColorMode();

  return (
    <WindowLayout>
      <Box sx={{
        width: '60%',
        marginLeft: 'auto',
        marginRight: 'auto',
        p: 2,
        py: 4,
        boxSizing: 'border-box',
      }}>
        <Flex sx={{
          justifyContent: 'space-between',
          alignItems: 'center',
        }}>
          <Heading as='h1'>
            Settings
          </Heading>
          <Link to='/' style={{
            color: 'inherit',
            textDecoration: 'none',
          }}>
            <Close sx={{
              transition: '.2s ease',
              ':hover': {
                transform: 'scale(1.1)',
                cursor: 'pointer',
              },
            }} />
          </Link>
        </Flex>
        <Divider my={3} />
        <Setting label='Dark mode?' toggled={colorMode === 'dark'} onToggle={() => setMode(colorMode === 'dark' ? 'light' : 'dark')} />
      </Box>
    </WindowLayout>
  );
}

export default Settings;