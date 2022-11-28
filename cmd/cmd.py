"""
Module providing the template for a command
"""

from cmd._helper.clisessionstate import CLISessionState
from typing import *

class Command(object):
    """
    A template command
    """

    def __init__(self, name: str, aliases: List[str] = [], description: str = ''):
        """
        Initializes a command with the specified name, aliases and description.
        """
        self.name: str = name
        self.aliases: List[str] = aliases
        self.description: str = description

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