"""
Module providing the template for a command
"""

from argparse import ArgumentError
from typing import List, Optional

from prompt_toolkit.completion.nested import NestedDict

from d4v1d.platforms.platform.cmd.argparser import ArgParser
from d4v1d.platforms.platform.cmd.clisessionstate import CLISessionState
from d4v1d.utils import io


class Command:
    """
    A template command
    """

    _parser: ArgParser
    """The argument parser for the command."""
    _needs_parsing: bool = False
    """Whether or not the command needs parsing."""

    def __init__(self, name: str, aliases: Optional[List[str]] = None, description: str = ''):
        """
        Initializes a command with the specified name, aliases and description.

        Args:
            name (str): The name of the command
            aliases (Optional[List[str]]): The aliases of the command. Defaults to None.
            description (str, optional): The description of the command. Defaults to ''.
        """
        self.name: str = name
        self.aliases: List[str] = aliases if aliases is not None else []
        self.description: str = description
        self._parser = ArgParser(self.name)

    def add_argument(self, *args, **kwargs) -> None:
        """
        Wrapper method for ``.parser.add_argument``.
        """
        self._needs_parsing = True
        self._parser.add_argument(*args, **kwargs)

    def available(self, state: CLISessionState) -> bool:  # pylint: disable=unused-argument
        """
        Should the command be shown in help given the current
        session state - i.e. is the command usable considering
        the current cli session state?

        Args:
            state (CLISessionState): The current session state.
        
        Returns:
            bool: Available or not?
        """
        return True

    def completer(self, state: CLISessionState) -> Optional[NestedDict]:  # pylint: disable=unused-argument
        """
        This method can be used to provide more information
        about the commands structure - i.e. it can be used
        to provide the terminal user with autocomplete
        functionality in case of some enum-like values.

        Args:
            state (CLISessionState): The current session state.

        Returns:
            Optional[NestedDict]: Optionally, completer information.
        """
        return None

    def execute(self, raw_args: List[str], argv: List[str], state: CLISessionState, *args, **kwargs) -> None:
        """
        Executes the command with the given arguments.
        The arguments defined in the argument parser are passed
        to this function as keyword arguments.

        Args:
            raw_args (List[str]): The raw arguments that were passed to the command.
            argv (List[str]): Extra arguments; i.e. arguments that weren't defined 
                using the argument parser.
            state (CLISessionState): The current session state.
        """

    def __call__(self, args: List[str], state: CLISessionState) -> None:
        """
        Execute this command - before doing so, however, parse
        the given arguments with the argument parser and pass
        them on as keyword arguments.

        Args:
            args (List[str]): The raw arguments that were passed to the command.
            state (CLISessionState): The current session state.
        """
        if self._needs_parsing:
            try:
                p_args, argv = self._parser.parse_known_args(args)
                self.execute(raw_args=args, argv=argv, state=state,
                            **dict(p_args._get_kwargs()))
            except (ValueError, ArgumentError) as e:
                io.e(e)
        else:
            self.execute(raw_args=args, argv=args, state=state)
