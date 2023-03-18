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
        self.add_argument('group_name', type=str, help='The name of the group to create. (e.g. "mygroup")')

    def available(self, state: CLISessionState) -> bool:
        """
        Can this command be used right now?
        """
        return bool(state.platform)

    def execute(self, group_name: str, raw_args: List[str], argv: List[str], state: CLISessionState) -> None:
        """
        Executes the command.

        Args:
            group_name (str): The name of the group to create.
            raw_args (List[str]): The raw arguments passed to the command.
            argv (List[str]): The extra arguments that weren't parsed.
            state (CLISessionState): The current session state.
        """
        if not state.platform:
            io.e('No platform selected. Use [bold]use[/bold] to select a platform.')
            return
        if group_name in state.platform.groups:
            io.e(f'Group [bold]{group_name}[/bold] already exists.')
            return
        state.platform.add_group(group_name)
        print(f'[green]Successfully created group [bold]{group_name}[/bold] for platform [bold]{state.platform.name}[/bold].[/green]')