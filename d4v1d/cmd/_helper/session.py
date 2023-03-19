"""
Custom prompt session - to allow updating
commands on the fly.
"""

import sys
import copy
from typing import Any, Dict, List, Optional, Tuple, Union

from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion.nested import NestedDict
from prompt_toolkit.formatted_text.html import HTML
from rich import print  # pylint: disable=redefined-builtin

from d4v1d import config
from d4v1d.cmd._helper.completer import CmdCompleter
from d4v1d.cmd._helper.validator import CmdValidator
from d4v1d.platforms.platform.cmd.clisessionstate import CLISessionState
from d4v1d.platforms.platform.cmd.cmd import Command


class CmdSession(PromptSession):
    """
    Custom prompt session - to allow updating
    commands on the fly.
    """

    cmds: Dict[str, Dict[str, Union[Command, Dict[str, Any]]]]
    """Cmd collections"""
    completer: CmdCompleter
    """Custom completer to auto-complete commands"""
    validator: CmdValidator
    """Validator to validate commands"""
    state: CLISessionState
    """The current state of the CLI session"""
    compl_dict: NestedDict
    """Dictionary for command completion"""

    __cmds: Dict[str, Union[Command, Dict[str, Any]]] = {}
    """All current commands - with expanded aliases"""

    def __init__(self, cmds: Dict[str, Union[Command, Dict[str, Any]]], *args,
                 complete_while_typing: Optional[bool] = None, **kwargs):
        """
        Create a new command prompt session.

        Args:
            cmds (Dict[str, Union[Command, Dict[str, Any]]]): The original commands to use.
            complete_while_tpying (Optional[bool]): Passed on to super(). 
                Default is using config.COMPLETE_WHILE_TYPING.
        """
        super().__init__(*args, completer=CmdCompleter.from_nested_dict({}),
                         validator=CmdValidator(self),
                         complete_while_typing=config.COMPLETE_WHILE_TYPING,
                         auto_suggest=AutoSuggestFromHistory(), **kwargs)
        self.completer.session = self
        self.cmds = {
            '__init__': cmds,
        }
        self.state = CLISessionState(self)
        self.refresh()

    def __del__(self) -> None:
        """
        Clean-up before finally exiting.
        """
        self.exit()

    def handle_forever(self) -> None:
        """
        Keep prompting the user for commands until they
        end the program.
        """
        while True:
            try:
                prompt: HTML = HTML(config.PROMPT.replace('%%', f'<aaa fg="Grey">:</aaa>{self.state.platform}' if self.state.platform else ''))
                self.handle(self.prompt(prompt))
            except KeyboardInterrupt:
                continue
            except EOFError:
                break

    def exit(self, code: int = 0) -> None:
        """
        Clean-up and stop prompting session.

        Args:
            code (int, optional): The exit code. Default is 0.
        """
        if self.state.platform is not None:
            self.remove(self.state.platform.name)
            del self.state.platform
            self.state.platform = None
        sys.exit(code)

    def handle(self, cmdline: str) -> None:
        """
        Handle some user input on the command line.

        Args:
            cmdline (str): The user's input.
        """
        if not cmdline.strip():
            return

        try:
            cmd, args = self[cmdline]
            cmd(args, state=self.state)
        except KeyError as e:
            # should never happen, since commands should
            # be validated before being executed
            print(f'[bold red][-][/bold red] {e}')

    def refresh(self) -> None:
        """
        Flush current collection of commands
        to sub-components - i.e. tell the validator
        and completer to update their commands.
        """
        self.__cmds.clear()
        for v in self.cmds.values():
            self.deep_merge(self.__cmds, self.__build_aliases(v))
        self.compl_dict = self.completer_dict()
        self.completer.update(self.compl_dict)

    def extend(self, coll_name: str, cmds: Dict[str, Union[Command, Dict[str, Any]]]) -> None:
        """
        Extend the session with more commands.

        Args:
            coll_name (str): The name of the command collection.
            cmds (Dict[str, Union[Command, Dict[str, Any]]]): The new commands.
        """
        self.cmds[coll_name] = cmds
        self.refresh()

    def remove(self, coll_name: str) -> None:
        """
        Remove a collection of commands.

        Args:
            coll_name (str): The name of the command collection.
        """
        self.cmds.pop(coll_name)
        self.refresh()

    def completer_dict(self) -> NestedDict:
        """
        Get a dictionary of commands for the completer.

        Returns:
            NestedDict: The dictionary of commands.
        """
        compl: NestedDict = {}
        self.__build_completer(compl, self.__cmds)
        return compl

    def deep_merge(self, a: Dict[str, Any], b: Dict[str, Any]) -> None:
        """
        Deep merges two dictionaries into the first one.

        Args:
            a (Dict[str, Any]): Dict a.
            b (Dict[str, Any]): Dict b.
        """
        for k, v in b.items():
            if isinstance(v, dict):
                self.deep_merge(a.setdefault(k, {}), v)
            else:
                # overwrite earlier entries w later ones
                # per default ...
                a[k] = v

    def parse(self, args: List[str]) -> Tuple[Union[Command, Dict[str, Union[Command, Dict[str, Any]]]], List[str]]:
        """
        Get a command / command dictionary in case of
        subcommands from the session.

        Args:
            args (List[str]): The CLI args.

        Raises:
            ValueError: If the command does not exist.

        Returns:
            Tuple[Command, List[str]]: The command / command dictionary and all
                remaining args.
        """
        _args: List[str] = args.copy()
        d: Dict[str, Union[Command, Dict[str, Any]]] = self.__cmds
        while isinstance(d, dict) and len(_args) > 0:
            cu: str = _args.pop(0)
            if cu not in d:
                raise KeyError(f'Unknown command: "{" ".join(args)}"')
            d = d[cu]
        if not isinstance(d, dict) and not isinstance(d, Command):
            raise KeyError(f'Incomplete command: "{" ".join(args)}"')
        return d, _args

    def __build_aliases(self, cmds: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extends the given CMD dictionary with entries
        for all aliases (at the moment only top-level
        aliases).

        Args:
            cmds (Dict[str, Any]): The dictionary of commands.
        """
        __cmds: Dict[str, Any] = copy.deepcopy(cmds)
        for v in __cmds.copy().values():
            if isinstance(v, Command):
                for a in v.aliases:
                    __cmds[a] = v
        return __cmds

    def __build_completer(self, compl: Dict[str, Union[None, Dict[str, Any]]], cmds: Dict[str, Union[Command, Dict[str, Any]]]) -> None:
        """
        Builds a completer dictionary from the specified
        dictionary of commands.

        Args:
            compl (Dict[str, Union[None, Dict[str, Any]]]): The completer dictionary of commands.
            cmds (Dict[str, Union[Command, Dict[str, Any]]]): The dictionary of commands.
        """
        for k, v in cmds.items():
            if isinstance(v, Command):
                compl[k] = None
            else:
                compl[k] = {}
                self.__build_completer(compl[k], cmds[k])

    def __getitem__(self, cmd: str) -> Tuple[Command, List[str]]:
        """
        Get a command from the session.

        Args:
            cmd (str): The name of the command.

        Raises:
            ValueError: If the command does not exist.
            TypeError: If the command actually requires sub-commands.

        Returns:
            Tuple[Command, List[str]]: The command & all args.
        """
        d, args = self.parse(cmd.strip().split())
        if isinstance(d, dict):
            raise TypeError(f'"{cmd}" has several sub-commands!')
        if not d.available(self.state):
            raise ValueError(f'"{cmd}" is not usable in the current context!')
        return d, args

    def __iadd__(self, other: Tuple[str, Dict[str, Union[Command, Dict[str, Any]]]]) -> "CmdSession":
        """
        Extend the session with more commands.

        Args:
            other (Tuple[str, Dict[str, Union[Command, Dict[str, Any]]]]): Name of the new command
                collection plus new commands.

        Returns:
            CmdSession: The session.
        """
        if not isinstance(other, tuple) or len(other) != 2 or not isinstance(other[0], str) or not isinstance(other[1], dict):
            raise ValueError('Invalid type for extending session - has to be a tuple of (<collection name>, <cmd collection>).')
        self.extend(*other)
        return self

    def __isub__(self, other: str) -> "CmdSession":
        """
        Remove a collection of commands.

        Args:
            other (str): The name of the command collection.

        Returns:
            CmdSession: The session.
        """
        if not isinstance(other, str):
            raise ValueError('Invalid type for removing collection - has to be a string (name of the collection).')
        self.remove(other)
        return self
