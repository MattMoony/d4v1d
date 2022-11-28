"""
Module for the exit command
"""

import sys
from cmd.cmd import Command
from cmd._helper.clisessionstate import CLISessionState
from typing import *

class Exit(Command):
    """
    The exit command
    """

    def __init__(self):
        """
        Initializes the exit command
        """
        super().__init__('exit', aliases=['quit',], description='Exits the program')

    def execute(self, args: List[str], state: CLISessionState) -> None:
        """
        Executes the exit command
        """
        sys.exit(0)