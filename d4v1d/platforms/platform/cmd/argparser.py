"""
Custom deriviation of ``argparse.ArgumentParser`` to
allow argument parser to be used in an interactive prompt
session instead of only when launching python scripts.
"""

import sys
from argparse import Action, ArgumentError, ArgumentParser
from typing import IO, List, Optional

from rich import print

from d4v1d.utils import io


class ArgParser(ArgumentParser):
    """
    Custom ``argparse.ArgumentParser`` to allow
    interactive CLI-parsing and handling - *importantly*,
    without **crashing** the program every time ...
    """

    __usage: Optional[str] = None
    """Optionally, static ``usage`` string."""

    def __init__(self, name: str) -> None:
        """
        Initialize a new command parser.

        Args:
            name (str): The name of the command.
        """
        super().__init__(prog=name, exit_on_error=False, conflict_handler='resolve')

    @property
    def usage(self) -> str:
        """
        Get the usage string for the command.

        Returns:
            str: The usage string.
        """
        return self.format_usage(no_style=True)

    @usage.setter
    def usage(self, value: str) -> None:
        """
        Set the usage string for the command.

        Args:
            value (str): The usage string.
        """
        self.__usage = value

    @property
    def help(self) -> str:
        """
        Get the help string for the command.

        Returns:
            str: The help string.
        """
        return self.format_help(no_style=True)

    def format_usage(self, no_style: bool = False) -> str:
        """
        Get the usage string for the command.

        Args:
            no_style (bool, optional): Don't use ``rich`` styling. Defaults to False.

        Returns:
            str: The usage string.
        """
        return self.__usage if self.__usage is not None \
               else f'{self.prog} {" ".join(self.__markup_action(a, no_style=no_style) for a in self._actions)}'
    
    def format_help(self, no_style: bool = False) -> str:
        """
        Get the help string for the command.

        Args:
            no_style (bool, optional): Don't use ``rich`` styling. Defaults to False.

        Returns:
            str: The help string.
        """
        positional: List[Action] = [ a for a in self._actions if not a.option_strings ]
        options: List[Action] = [ a for a in self._actions if a.option_strings ]
        return io._l(f'{"" if no_style else "[bold]"}Usage:{"" if no_style else "[/bold]"} {self.format_usage(no_style=no_style)}') +\
               ('\n' + io._l(f'{"" if no_style else "[bold]"}Positional arguments:{"" if no_style else "[/bold]"}') +\
               '\n' + '\n'.join(self.__positional_help(a, no_style=no_style) for a in positional) if positional else '') +\
               ('\n' + io._l(f'{"" if no_style else "[bold]"}Options:{"" if no_style else "[/bold]"}') +\
               '\n' + '\n'.join(self.__option_help(a, no_style=no_style) for a in options) if options else '')

    def error(self, message: str) -> None:
        """
        Helper method for overriding part of the ``argparse.ArgumentParser``
        to NOT MAKE IT EXIT ON ERROR; because the option alone doesn't seem
        to suffice for some reason ...

        Args:
            message (str): Some error message.
        """
        raise ValueError(f'{message} (use -h for help). [bold]Usage:[/bold] {self.format_usage()}')
    
    def exit(self, message: Optional[str] = None, status: int = 0, *args, **kwargs) -> None:
        """
        Helper method for overriding part of the ``argparse.ArgumentParser``
        to NOT MAKE IT EXIT ON ERROR; because the option alone doesn't seem
        to suffice for some reason ...

        Args:
            message (Optional[str]): Some error message.
            status (int, optional): The exit status. Defaults to 0.
        """
        pass

    def print_usage(self, file: IO[str] | None = None) -> None:
        """
        Helper method for overriding part of the ``argparse.ArgumentParser``
        to have custom, more "theme-appropriate" usage messages.

        Args:
            file (IO[str] | None, optional): The file to print to. Defaults to None.
        """
        if file is None or file == sys.stdout:
            print(self.format_usage())
            return
        file.write(self.usage)

    def print_help(self, file: IO[str] | None = None) -> None:
        """
        Helper method for overriding part of the ``argparse.ArgumentParser``
        to have custom, more "theme-appropriate" error messages.

        Args:
            file (IO[str] | None, optional): The file to print to. Defaults to None.
        """
        if file is None or file == sys.stdout:
            print(self.format_help())
            return
        file.write(self.help)

    def __markup_action(self, action: Action, no_style: bool = False) -> str:
        """
        Get a string representation of the action - used, e.g.,
        in ``usage``.

        Args:
            action (Action): The action.
            no_style (bool, optional): Don't use ``rich`` style tags. Defaults to using them.

        Returns:
            str: The string representation.
        """
        mark: str = f'{"" if no_style else "[italic]"}{action.option_strings[0]}{" <" + action.dest + ">" if action.nargs != 0 else ""}{"" if no_style else "[/italic]"}' \
                    if action.option_strings \
                    else f'<{action.dest}>'
        return mark if no_style or action.required else f'[dim]{mark}[/dim]'
    
    def __positional_help(self, action: Action, no_style: bool = False) -> str:
        """
        Generate the help string for a positional argument
        as used in the ``help`` command.

        Args:
            action (Action): The action.
            no_style (bool, optional): Don't use ``rich`` style tags. Defaults to using them.

        Returns:
            str: The string representation.
        """
        return io.__(f'{"" if no_style else "[bold]"}{action.dest.ljust(24)}{"" if no_style else "[/bold]"} {self.__action_help_sub(action, no_style=no_style)}')
    
    def __option_help(self, action: Action, no_style: bool = False) -> str:
        """
        Generate the help string for an option as used in the
        ``help`` command.

        Args:
            action (Action): The action.
            no_style (bool, optional): Don't use ``rich`` style tags. Defaults to using them.

        Returns:
            str: The string representation.
        """
        return io.__(f'{"" if no_style else "[bold]"}{"/".join(action.option_strings).ljust(24)}{" required." if action.required else ""}{"" if no_style else "[/bold]"} {self.__action_help_sub(action, no_style=no_style)}')

    def __action_help_sub(self, action: Action, no_style: bool = False) -> str:
        """
        Generate the help string for an action as used in the
        ``help`` command - used by positional & optional args.

        Args:
            action (Action): The action.
            no_style (bool, optional): Don't use ``rich`` style tags. Defaults to using them.
        
        Returns:
            str: The string representation.
        """
        return f'{action.help if action.help else ""}' +\
               (f' {"" if no_style else "[dim]"}Default is {"" if no_style else "[italic]"}{action.default}.{"" if no_style else "[/italic][/dim]"}' if action.default is not None and action.dest != 'help' else '')

    def __str__(self) -> str:
        """
        Get a string representation of the command.

        Returns:
            str: The string representation.
        """
        return f'ArgParser<<{self.usage}>>'

    def __repr__(self) -> str:
        """
        Get a string representation of the command.

        Returns:
            str: The string representation.
        """
        return f'<{self}>'
