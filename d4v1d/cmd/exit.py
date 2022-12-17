"""
Module for the exit command
"""

import sys
from d4v1d.platforms.platform.cmd import Command, CLISessionState
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