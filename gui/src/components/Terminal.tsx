import * as React from 'react';
import { useState, useEffect } from 'react';
import { Box } from '@theme-ui/components';
import { Flex, Input, Label, Text } from 'theme-ui';

/** @jsxImportSource theme-ui */

type TerminalProps = {
  height: number;
}

type TerminalState = {
  log: string;
  sticky: boolean;
}

// const Terminal = ({ height, }: TerminalProps) => {

//   const [log, setLog] = useState('');
//   const [sticky, setSticky] = useState(true);
//   const [receiver, setReceiver] = useState(false);
//   const input: React.MutableRefObject<HTMLInputElement> = React.useRef();
//   const output: React.MutableRefObject<HTMLDivElement> = React.useRef();
  
//   useEffect(() => {
//     // if (!receiver) {
//       // setReceiver(true);
//       // console.log('setting again!');
//       window.api.receive('fromMain', 'cli', (action: string, ...args: any[]) => {
//         if (typeof args[0] === 'string') {
//           console.log(log);
//           setLog(log + '\n' + args[0]);
//           if (sticky && output.current) output.current.scrollTo(0, output.current.scrollHeight);
//         }
//       });
//     // }
//   });

//   const handleScroll = () => {
//     if (output.current) {
//       if (output.current.scrollTop + output.current.clientHeight === output.current.scrollHeight) setSticky(true);
//       else setSticky(false);
//     }
//   };

//   const handleInput = (e: React.KeyboardEvent) => {
//     if (e.key === 'Enter') {
//       if (input.current) {
//         window.api.send('toMain', 'cli', input.current!.value.trim());
//         input.current!.value = '';
//       }
//     }
//   };

//   return (
//     <Flex sx={{
//       flexDirection: 'column',
//       justifyContent: 'stretch',
//       alignItems: 'stretch',
//       height,
//       width: '100%',
//       boxSizing: 'border-box',
//       p: 3,
//       fontFamily: 'monospace',
//     }}>
//       <Box ref={output} onScroll={handleScroll} sx={{
//         flex: 1,
//         minHeight: 0,
//         overflow: 'auto',
//         whiteSpace: 'pre-wrap',
//         '::-webkit-scrollbar': {
//           width: 8,
//         },
//         '::-webkit-scrollbar-track': {
//           backgroundColor: 'background',
//         },
//         '::-webkit-scrollbar-thumb': {
//           boxShadow: 'inset 0 0 6px rgba(0, 0, 0, .4)',
//         },
//       }}>
//         {log}
//       </Box>
//       <Flex sx={{
//         justifyContent: 'stretch',
//         alignItems: 'center',
//         borderTop: '3px solid',
//         borderColor: 'background',
//         pt: 3,
//         mt: 3,
//       }}>
//         <Box sx={{
//           color: 'lightGray',
//         }}>
//           <span sx={{ color: 'secondary', }}>matt_moony</span>@<span sx={{ color: 'primary', }}>d4v1d</span>
//         </Box>
//         <Input ref={input} onKeyUp={handleInput} sx={{
//           border: '2px solid',
//           borderColor: 'background',
//           width: 'auto',
//           flexGrow: 1,
//           marginLeft: 2,
//           p: 2,
//           fontFamily: 'monospace',
//           fontSize: 1,
//           color: 'lightGray',
//           ':focus': {
//             outline: 'none',
//           }
//         }} />
//       </Flex>
//     </Flex>
//   );
// }

class Terminal extends React.Component<TerminalProps, TerminalState> {
  private output: HTMLDivElement;
  private input: HTMLInputElement;

  constructor(props) {
    super(props);
    this.state = {
      log: '',
      sticky: true,
    };
  }

  public componentDidMount() {
    window.api.receive('fromMain', 'cli', (action: string, ...args: any[]) => {
      if (typeof args[0] === 'string') {
        this.setState({ log: this.state.log + atob(args[0]), })
        if (this.state.sticky && this.output) this.output.scrollTo(0, this.output.scrollHeight);
      }
    });
  }

  private handleScroll () {
    if (this.output) {
      if (this.output.scrollTop + this.output.clientHeight === this.output.scrollHeight) this.setState({ sticky: true, });
      else this.setState({ sticky: false, });
    }
  }

  private handleInput (e: React.KeyboardEvent) {
    if (e.key === 'Enter') {
      if (this.input) {
        this.setState({ 
          log: this.state.log + `${this.input!.value.trim()}\n`, 
        }, () => {
          window.api.send('toMain', 'cli', this.input!.value.trim());
          this.input!.value = '';
        });
      }
    }
  }

  public render() {
    return (
      <Flex sx={{
        flexDirection: 'column',
        justifyContent: 'stretch',
        alignItems: 'stretch',
        height: this.props.height,
        width: '100%',
        boxSizing: 'border-box',
        p: 3,
        fontFamily: 'monospace',
      }}>
        <Box ref={e => this.output = e} onScroll={this.handleScroll.bind(this)} sx={{
          flex: 1,
          minHeight: 0,
          overflow: 'auto',
          whiteSpace: 'pre-wrap',
          '::-webkit-scrollbar': {
            width: 8,
          },
          '::-webkit-scrollbar-track': {
            backgroundColor: 'background',
          },
          '::-webkit-scrollbar-thumb': {
            boxShadow: 'inset 0 0 6px rgba(0, 0, 0, .4)',
          },
        }}>
          {this.state.log}
        </Box>
        <Flex sx={{
          justifyContent: 'stretch',
          alignItems: 'center',
          borderTop: '3px solid',
          borderColor: 'background',
          pt: 3,
          mt: 3,
        }}>
          <Box sx={{
            color: 'lightGray',
          }}>
            <span sx={{ color: 'secondary', }}>matt_moony</span>@<span sx={{ color: 'primary', }}>d4v1d</span>
          </Box>
          <Input ref={e => this.input = e} onKeyUp={this.handleInput.bind(this)} sx={{
            border: '2px solid',
            borderColor: 'background',
            width: 'auto',
            flexGrow: 1,
            marginLeft: 2,
            p: 2,
            fontFamily: 'monospace',
            fontSize: 1,
            color: 'lightGray',
            ':focus': {
              outline: 'none',
            }
          }} />
        </Flex>
      </Flex>
    );
  }
}

export default Terminal;