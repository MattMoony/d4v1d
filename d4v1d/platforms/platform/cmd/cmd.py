"""
Module providing the template for a command
"""

from typing import *

from prompt_toolkit.completion.nested import NestedDict

from .clisessionstate import CLISessionState


class Command(object):
    """
    A template command
    """

    def __init__(self, name: str, aliases: List[str] = [], description: str = ''):
        """
        Initializes a command with the specified name, aliases and description.

        Args:
            name (str): The name of the command
            aliases (List[str], optional): The aliases of the command. Defaults to [].
            description (str, optional): The description of the command. Defaults to ''.
        """
        self.name: str = name
        self.aliases: List[str] = aliases
        self.description: str = description

    def available(self, state: CLISessionState) -> bool:
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
    
    def completer(self, state: CLISessionState) -> Optional[NestedDict]:
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

    def execute(self, args: List[str], state: CLISessionState) -> None:
        """
        Executes the command with the specified arguments.
        """
        pass

    def __call__(self, args: List[str], state: CLISessionState) -> None:
        """
        Calls the execute method.
        """
        self.execute(args, state=state)