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
from prompt_toolkit.document import Document
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.validation import Validator, ValidationError
from typing import *

CMDS: Dict[str, Any] = {
    'exit': ExitCommand(),
}
CMDS['help'] = HelpCommand(CMDS)

class CmdValidator(Validator):
    """
    Validator for the command prompt
    """
    def validate(self, document: Document) -> None:
        """
        Validate some input

        Args:
            document (Document): The input to validate
        """
        if not document.text.strip():
            return
        try:
            get_cmd(document.text)
        except ValueError as e:
            raise ValidationError(message=str(e))

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

def get_cmd(cmd: str) -> Tuple[Command, List[str]]:
    """
    Returns the command specified by the given arguments
    plus the remaining arguments.
    """
    args: List[str] = cmd.split()
    d: Union[Dict[str, Any], Command] = CMDS
    while isinstance(d, dict) and len(args) > 0:
        cu: str = args.pop(0)
        if cu not in d:
            raise ValueError(f'Unknown command: "{cmd}"')
        d = d[cu]
    if not isinstance(d, Command):
        raise ValueError(f'Incomplete command: "{cmd}"')
    return d, args

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
    if not inp.strip():
        return
    try:
        cmd, args = get_cmd(inp)
        cmd(args)
    except ValueError as e:
        # should never happen, since commands should
        # be validated before being executed
        print(f'[-] {e}')

def start() -> None:
    """
    Starts handling user input.
    """
    __build_aliases()
    session = PromptSession(
        completer=completer(), 
        complete_while_typing=config.COMPLETE_WHILE_TYPING,
        validator=CmdValidator(),
        auto_suggest=AutoSuggestFromHistory(),
    )
    while True:
        try:
            handle(session.prompt(config.PROMPT))
        except KeyboardInterrupt:
            continue
        except EOFError:
            break