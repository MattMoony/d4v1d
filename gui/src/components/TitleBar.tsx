import * as React from 'react';
import { useEffect } from 'react';
import * as style from './TitleBar.module.scss';
import { Icon, IconifyIcon } from '@iconify/react';
import closeCircleOutlined from '@iconify-icons/ant-design/close-circle-outlined';
import chromeMinimize from '@iconify-icons/codicon/chrome-minimize';
import chromeMaximize from '@iconify-icons/codicon/chrome-maximize';
import chromeRestore from '@iconify-icons/codicon/chrome-restore';
import spyLine from '@iconify-icons/ri/spy-fill';
import { Box, Container, Flex, Heading, IconButton } from 'theme-ui';

/** @jsxImportSource theme-ui */

interface IconDef {
  icon: any;
  onClick: () => void;
};

const TitleBar = () => {
  const icons: IconDef[] = [
    { icon: chromeMinimize, onClick: () => window.api.send('toMain', 'minimize'), },
    { icon: chromeMaximize, onClick: () => window.api.send('toMain', 'maximize'), },
    { icon: closeCircleOutlined, onClick: () => window.api.send('toMain', 'close'), },
  ];

  return (
    <Flex sx={{
      p: 1,
      px: 2,
      userSelect: 'none',
      WebkitUserSelect: 'none',
      WebkitAppRegion: 'drag',
      backgroundColor: 'primary',
      borderBottom: '5px solid',
      borderColor: 'muted',
      fontSize: 2,
      alignItems: 'center',
      justifyContent: 'space-between',
    }}>
      <Flex sx={{
        flex: '1 1 auto',
        justifyContent: 'left',
        alignItems: 'center',
      }}>
        <Flex sx={{
          fontSize: 3,
          justifyContent: 'center',
          alignItems: 'center',
          marginRight: 1,
          color: 'text',
        }}>
          <Icon icon={spyLine} />
        </Flex>
        <Heading as='h3'>
          d4v1d
        </Heading>
      </Flex>
      {icons.map((i, x) => 
        <IconButton sx={{
          fontSize: 3,
          WebkitAppRegion: 'no-drag',
          transition: '.2s ease',
          ":hover": {
            color: 'secondary',
            cursor: 'pointer',
          },
        }} key={x} onClick={i.onClick}>
          <Icon icon={i.icon} />
        </IconButton>)
      }
    </Flex>
  );
};

export default TitleBar;