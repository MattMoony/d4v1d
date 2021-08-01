import * as React from 'react';
import { useState } from 'react';
import { Box, Flex, Grid, Heading, useThemeUI } from 'theme-ui';
import { Treebeard } from 'react-treebeard';
import WindowLayout from '../components/WindowLayout';
import { useEffect } from 'react';
import { navigate } from '@reach/router';

const Index = () => {
  useEffect(() => {
    window.addEventListener('keyup', (e: React.KeyboardEvent) => {
      switch (e.key) {
        case ',':
          if (e.ctrlKey) navigate('/settings/');
          break;
      }
    });
  });

  const [tree, setTree] = useState({
    name: 'd4v1d',
    toggled: true,
    children: [
      {
        name: 'test',
        children: [
          { name: 'a', },
          { name: 'b', },
        ]
      },
      {
        name: 'test2',
      }
    ],
  });
  const [cursor, setCursor] = useState(null);

  const onToggle = (node, toggled) => {
    if (cursor) cursor.active = false;
    node.active = true;
    if (node.children) node.toggled = toggled;
    setCursor(node);
    setTree(Object.assign({}, tree));
  };

  const context = useThemeUI();
  const { theme, } = context;

  return (
    <WindowLayout>
      <Flex sx={{
        width: '100%',
        height: '100%',
      }}>
        <Box sx={{
          maxWidth: '10em',
          width: '50%',
          borderRight: '3px solid',
          borderColor: 'muted',
        }}>
          <Treebeard
            data={tree}
            onToggle={onToggle}
            style={{
              tree: {
                base: {
                  listStyle: 'none',
                  backgroundColor: theme.rawColors.background,
                  margin: 0,
                  padding: 0,
                  color: theme.rawColors.text,
                  fontFamily: 'lucida grande ,tahoma,verdana,arial,sans-serif',
                  fontSize: '14px'
                },
                node: {
                  base: {
                    position: 'relative'
                  },
                  link: {
                    cursor: 'pointer',
                    position: 'relative',
                    padding: '0px 5px',
                    display: 'block'
                  },
                  activeLink: {
                    background: theme.rawColors.muted,
                  },
                  toggle: {
                    base: {
                      position: 'relative',
                      display: 'inline-block',
                      verticalAlign: 'top',
                      marginLeft: '-5px',
                      height: '24px',
                      width: '24px'
                    },
                    wrapper: {
                      position: 'absolute',
                      top: '50%',
                      left: '50%',
                      margin: '-7px 0 0 -7px',
                      height: '14px'
                    },
                    height: 14,
                    width: 14,
                    arrow: {
                      fill: theme.rawColors.text,
                      strokeWidth: 0
                    }
                  },
                  header: {
                    base: {
                      display: 'inline-block',
                      verticalAlign: 'top',
                      color: theme.rawColors.text,
                    },
                    connector: {
                      width: '2px',
                      height: '12px',
                      borderLeft: 'solid 2px black',
                      borderBottom: 'solid 2px black',
                      position: 'absolute',
                      top: '0px',
                      left: '-21px'
                    },
                    title: {
                      lineHeight: '24px',
                      verticalAlign: 'middle'
                    }
                  },
                  subtree: {
                    listStyle: 'none',
                    paddingLeft: '19px'
                  },
                  loading: {
                    color: theme.rawColors.secondary,
                  }
                }
              }
            }}
          />
        </Box>
        <Box p={4} sx={{
          flex: 1,
          backgroundColor: 'muted',
        }}>
          <Heading>
            Hello World!
          </Heading>
        </Box>
      </Flex>
    </WindowLayout>
  );
}

export default Index;