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
from prompt_toolkit.completion.nested import NestedCompleter, NestedDict
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.validation import Validator, ValidationError
from d4v1d.platforms.platform.cmd import Command, CLISessionState
from typing import *

__CMDS: Dict[str, Any] = {}
"""Local copy of all available commands - with expanded aliases"""
__COMPLETER_CMDS: Dict[str, Any] = {}
"""Completer dictionary of all commands"""

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

class CmdCompleter(NestedCompleter):
    """
    Custom completer - to allow updating
    commands on the fly.
    """

    raw_data: NestedDict

    @classmethod
    def from_nested_dict(cls, data: NestedDict) -> "NestedCompleter":
        completer = super().from_nested_dict(data)
        completer.raw_data = data
        return completer

    def update(self, data: NestedDict) -> None:
        """
        Update the completer with new commands.

        Args:
            data (NestedDict): The new commands
        """
        self.options = NestedCompleter.from_nested_dict(data).options

    def reset(self) -> None:
        """
        Reset the completer to the original commands
        """
        self.options = NestedCompleter.from_nested_dict(self.raw_data).options

class CmdSession(PromptSession):
    """
    Custom prompt session - to allow updating
    commands on the fly.
    """

    completer: CmdCompleter

def build_aliases(cmds: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extends the given CMD dictionary with entries
    for all aliases (at the moment only top-level
    aliases).
    """
    __cmds: Dict[str, Any] = copy.deepcopy(cmds)
    for v in __cmds.copy().values():
        if isinstance(v, Command):
            for a in v.aliases:
                __cmds[a] = v
    return __cmds

def __build_aliases() -> None:
    """
    Extends the __CMDS dictionary with aliases
    (at the moment, only "top-level" aliases
    are supported)
    """
    global __CMDS
    __CMDS = build_aliases(CMDS)

def __reset_completer() -> None:
    """
    Reset the completer dictionary of all commands
    """
    for k, v in __COMPLETER_CMDS.items():
        del __COMPLETER_CMDS[k]

def build_completer(compl: Dict[str, Any], cmds: Dict[str, Any]) -> None:
    """
    Builds a completer dictionary from the specified
    dictionary of commands.

    Args:
        compl (Dict[str, Any]): The completer dictionary of commands
        cmds (Dict[str, Any]): The dictionary of commands
    """
    for k, v in cmds.items():
        if isinstance(v, Command):
            compl[k] = None
        else:
            compl[k] = {}
            build_completer(compl[k], cmds[k])

def get_cmd(cmd: str) -> Tuple[Command, List[str]]:
    """
    Returns the command specified by the given arguments
    plus the remaining arguments.

    Args:
        cmd (str): The command to get
    """
    args: List[str] = cmd.split()
    d: Union[Dict[str, Any], Command] = __CMDS
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
    global __COMPLETER_CMDS
    build_completer(__COMPLETER_CMDS, __CMDS)
    return CmdCompleter.from_nested_dict(__COMPLETER_CMDS)

def refresh() -> None:
    """
    Refresh the session - since the available commands
    have changed
    """
    __build_aliases()
    __reset_completer()
    build_completer(__COMPLETER_CMDS, __CMDS)

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
    state: CLISessionState = CLISessionState(session)
    while True:
        try:
            prompt: HTML = HTML(config.PROMPT.replace('%%', f'<aaa fg="Grey">:</aaa>{state.platform}' if state.platform else ''))
            handle(session.prompt(prompt), state)
        except KeyboardInterrupt:
            continue
        except EOFError:
            break