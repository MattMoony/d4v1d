"""
Module responsible for receiving and processing 
commands from the user.
"""

import copy
from rich import print
import d4v1d.config as config
import d4v1d.platforms as platform
from d4v1d.cmd._helper import CMDS
from prompt_toolkit import PromptSession
from prompt_toolkit.document import Document
from prompt_toolkit.formatted_text.html import HTML
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.validation import Validator, ValidationError
from d4v1d.platforms.platform.cmd import Command, CLISessionState
from typing import *

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

    Args:
        cmds (Dict[str, Any]): The dictionary of commands
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

    Args:
        cmd (str): The command to get
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

def handle(inp: str, state: CLISessionState) -> None:
    """
    Handles the specified user input.

    Args:
        inp (str): The user input
        state (CLISessionState): The current state of the CLI session
    """
    if not inp.strip():
        return
    try:
        cmd, args = get_cmd(inp)
        cmd(args, state=state)
    except ValueError as e:
        # should never happen, since commands should
        # be validated before being executed
        print(f'[bold red][-][/bold red] {e}')

def start() -> None:
    """
    Starts handling user input.
    """
    __build_aliases()
    session: PromptSession = PromptSession(
        completer=completer(), 
        complete_while_typing=config.COMPLETE_WHILE_TYPING,
        validator=CmdValidator(),
        auto_suggest=AutoSuggestFromHistory(),
    )
    state: CLISessionState = CLISessionState()
    while True:
        try:
            prompt: HTML = HTML(config.PROMPT.replace('%%', f' <aaa fg="DarkGrey">{state.platform}</aaa>' if state.platform else ''))
            handle(session.prompt(prompt), state)
        except KeyboardInterrupt:
            continue
        except EOFError:
            break