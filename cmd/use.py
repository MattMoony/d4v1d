"""
Module for the use command - used 
to switch between platforms
"""

import platforms
from rich import print
from cmd.cmd import Command
from cmd._helper.clisessionstate import CLISessionState
from platforms.platform import Platform
from typing import *

class Use(Command):
    """
    The use command
    """

    def __init__(self):
        """
        Initializes the use command
        """
        super().__init__('use', aliases=['switch',], description='Switches between platforms')

    def execute(self, args: List[str], state: CLISessionState) -> None:
        """
        Executes the use command

        Args:
            args (List[str]): The arguments
            state (CLISessionState): The session state
        """
        if len(args) == 0:
            if state.platform is not None:
                state.platform = None
                print(f'[bold grey53][*][/bold grey53] Not using any platform anymore ...')
            return

        platform: str = args.pop(0).lower()
        if any(p for n, p in platforms.PLATFORMS.items() if n.lower() == platform):
            state.platform = platform
            print(f'[bold grey53][*][/bold grey53] Switched to platform [bold]{platform}[/bold]')
        else:
            print(f'[bold red][-][/bold red] Platform [bold]{platform}[/bold] does not exist')