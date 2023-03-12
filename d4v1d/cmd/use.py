"""
Module for the use command - used 
to switch between platforms
"""

from rich import print
import d4v1d.platforms as platforms
from d4v1d.platforms.platform import Platform
from d4v1d.platforms.platform.cmd import Command, CLISessionState
from types import ModuleType
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
                state.session.completer.reset()
                del state.platform
                state.platform = None
                print(f'[bold grey53][*][/bold grey53] Not using any platform anymore ...')
            return

        platform: str = args.pop(0).lower()
        try:
            p: ModuleType = next(p for n, p in platforms.PLATFORMS.items() if n.lower() == platform)
            if state.platform:
                del state.platform
            state.platform = p.init()
            state.session.completer.update(state.platform.cmds)
            print(f'[bold grey53][*][/bold grey53] Switched to platform [bold]{platform}[/bold]')
        except StopIteration:
            print(f'[bold red][-][/bold red] Platform [bold]{platform}[/bold] does not exist')