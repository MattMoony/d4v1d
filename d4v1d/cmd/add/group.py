"""
Creates a new group
"""

from rich import print
from d4v1d.utils import io
from d4v1d.platforms.platform.cmd import Command, CLISessionState
from typing import *

class AddGroup(Command):
    """
    Creates a new group
    """
    
    def __init__(self):
        """
        Initializes the command.
        """
        super().__init__('add group', description='Create a new group for the currently selected platform.')

    def execute(self, args: List[str], state: CLISessionState) -> None:
        """
        Executes the command.
        """
        if not state.platform:
            io.e('No platform selected. Use [bold]use[/bold] to select a platform.')
            return
        if not args:
            io.e(f'Missing group name. [bold]Usage:[/bold] add group <group name>')
            return
        if args[0] in [g.name for g in state.platform.groups]:
            io.e(f'Group [bold]{args[0]}[/bold] already exists.')
            return
        state.platform.add_group(args[0])
        print(f'[green]Successfully created group [bold]{args[0]}[/bold] for platform [bold]{state.platform.name}[/bold].[/green]')