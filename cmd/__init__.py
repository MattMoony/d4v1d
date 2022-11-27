"""
Module responsible for receiving and processing 
commands from the user.
"""

import copy
import config
from rich import print
from cmd.cmd import Command
from cmd.help import HelpCommand
from cmd.exit import ExitCommand
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import NestedCompleter
from typing import *

CMDS: Dict[str, Any] = {
    'exit': ExitCommand(),
}
CMDS['help'] = HelpCommand(CMDS)

def __build_aliases() -> None:
    """
    Extends the CMDS dictionary with aliases
    (at the moment, only "top-level" aliases
    are supported)
    """
    for k, v in CMDS.copy().items():
        if isinstance(v, Command):
            for a in v.aliases:
                CMDS[a] = v

def __build_completer(cmds: Dict[str, Any]) -> None:
    """
    Builds a completer dictionary from the specified
    dictionary of commands.
    """
    for k, v in cmds.items():
        if isinstance(v, Command):
            cmds[k] = None
        else:
            __build_completer(v)

def completer() -> NestedCompleter:
    """
    Returns a NestedCompleter object with all
    available commands.
    """
    d: Dict[str, Any] = copy.deepcopy(CMDS)
    __build_completer(d)
    return NestedCompleter.from_nested_dict(d)

def handle(inp: str) -> None:
    """
    Handles the specified user input.
    """
    args: List[str] = inp.split()
    d: Union[Dict[str, Any], Command] = CMDS
    while isinstance(d, dict) and len(args) > 0:
        cu: str = args.pop(0)
        if cu not in d:
            print(f'[-] Unknown command: [italic]{cu}[/italic]. Enter [bold]help[/bold] to see all available commands ...')
            return
        d = d[cu]
    if not isinstance(d, Command):
        print(f'[-] Incomplete command: [italic]{cu}[/italic]. Enter [bold]help {cu}[/bold] to see how to use it ...')
        return
    d(args)

def start() -> None:
    """
    Starts handling user input.
    """
    __build_aliases()
    session = PromptSession(completer=completer(), complete_while_typing=config.COMPLETE_WHILE_TYPING)
    while True:
        try:
            handle(session.prompt(config.PROMPT))
        except KeyboardInterrupt:
            continue
        except EOFError:
            break