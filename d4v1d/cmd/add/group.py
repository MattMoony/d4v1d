"""
Creates a new group
"""

from typing import List

from rich import print

from d4v1d.platforms.platform.cmd import CLISessionState, Command
from d4v1d.utils import io


class AddGroup(Command):
    """
    Creates a new group
    """
    
    def __init__(self):
        """
        Initializes the command.
        """
        super().__init__('add group', description='Create a new group for the currently selected platform.')

    def available(self, state: CLISessionState) -> bool:
        """
        Can this command be used right now?
        """
        return bool(state.platform)

    def execute(self, raw_args: List[str], argv: List[str], state: CLISessionState) -> None:
        """
        Executes the command.
        """
        if not state.platform:
            io.e('No platform selected. Use [bold]use[/bold] to select a platform.')
            return
        if not raw_args:
            io.e(f'Missing group name. [bold]Usage:[/bold] add group <group name>')
            return
        if raw_args[0] in state.platform.groups:
            io.e(f'Group [bold]{raw_args[0]}[/bold] already exists.')
            return
        state.platform.add_group(raw_args[0])
        print(f'[green]Successfully created group [bold]{raw_args[0]}[/bold] for platform [bold]{state.platform.name}[/bold].[/green]')