"""
Search the currently loaded platforms for the
description of a specific user
"""

from rich import print
from d4v1d.platforms.platform.errors import PlatformError
from d4v1d.utils import io
from d4v1d.platforms.platform.info import Info
from d4v1d.platforms.platform.cmd.clisessionstate import CLISessionState
from d4v1d.platforms.platform.cmd.cmd import Command
from typing import *

class ShowDescription(Command):
    """
    Search the currently loaded platforms for the
    description of a specific user
    """

    def __init__(self):
        """
        Initializes the command.
        """
        super().__init__('show description', description='Show a users description (from the currently enabled platform).')

    def available(self, state: CLISessionState) -> bool:
        """
        Can it be used rn?
        """
        return bool(state.platform)

    def execute(self, args: List[str], state: CLISessionState) -> None:
        """
        Executes the command.
        """
        if not args:
            io.e('Missing username. [bold]Usage:[/bold] show description <username>')
            return
        if not state.platform:
            io.e('No platform loaded. Enable one with the [bold]use[/bold] command.')
            return
        try:
            d: Info[str] = state.platform.get_user_description(args[0])
            print(f'[bold]Description of {args[0]} @ {d.date.isoformat()}:[/bold]\n{d.value}')
        except PlatformError as e:
            io.e(f'[bold]{e.__class__.__name__}{":[/bold] "+str(e) if str(e) else "[/bold]"}')
            return