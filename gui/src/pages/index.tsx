import * as React from 'react';
import { useState } from 'react';
import { Box, Flex, Grid, Heading, IconButton, Label, useThemeUI } from 'theme-ui';
import { Treebeard } from 'react-treebeard';
import WindowLayout from '../components/WindowLayout';
import { useEffect } from 'react';
import { navigate } from '@reach/router';
import terminalIcon from '@iconify-icons/bi/terminal';
import Icon from '@iconify/react';
import Terminal from '../components/Terminal';

const Index = () => {
  useEffect(() => {
    window.addEventListener('keyup', (e: React.KeyboardEvent) => {
      switch (e.key) {
        case ',':
          if (e.ctrlKey) navigate('/settings/');
          break;
        case '.':
          if (e.ctrlKey) setTermVisible(!termVisible);
          break;
      }
    });
    window.addEventListener('resize', () => {
      setHeight(window.document.body.getBoundingClientRect().height);
    });
    setHeight(window.document.body.getBoundingClientRect().height);
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
  const [termVisible, setTermVisible] = useState(false);
  const [height, setHeight] = useState(0);

  return (
    <WindowLayout>
      <Flex sx={{
        width: '100%',
        height: '100%',
        flexDirection: 'column',
        overflowY: 'hidden',
      }}>
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
        <Flex sx={{
          backgroundColor: 'transparent',
          position: 'relative',
          transition: '.2s ease',
          // transform: `translateY(${termVisible ? '0' : '100%'})`,
          maxHeight: termVisible ? Math.floor(height/2) : 3,
          height: '50%',
          flexDirection: 'column',
          justifyContent: 'stretch',
          boxSizing: 'border-box',
        }}>
          <IconButton sx={{
            fontSize: 2,
            backgroundColor: 'gray',
            position: 'absolute',
            borderTop: '3px solid',
            borderLeft: '3px solid',
            borderRight: '3px solid',
            borderColor: 'primary',
            borderRadius: '15% 15% 0 0',
            top: -29,
            right: 10,
            zIndex: 10,
            transition: '.2s ease',
            ':hover': {
              color: 'primary',
              cursor: 'pointer',
            }
          }} onClick={() => setTermVisible(!termVisible)}>
            <Icon icon={terminalIcon} />
          </IconButton>
          <Box sx={{
            backgroundColor: 'gray',
            borderTop: '3px solid',
            borderColor: 'primary',
            flexGrow: 1,
          }}>
            <Terminal height={Math.floor((height/2)*.9)} />
          </Box>
        </Flex>
      </Flex>
    </WindowLayout>
  );
}

export default Index;