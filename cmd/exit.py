"""
Module for the exit command
"""

import sys
from cmd.cmd import Command
from typing import *

class ExitCommand(Command):
    """
    The exit command
    """

    def __init__(self):
        """
        Initializes the exit command
        """
        super().__init__('exit', aliases=['quit',], description='Exits the program')

    def execute(self, args: List[str]) -> None:
        """
        Executes the exit command
        """
        sys.exit(0)