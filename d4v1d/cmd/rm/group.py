"""
Removes a group
"""

from typing import List, Optional

from prompt_toolkit.completion.nested import NestedDict
from rich import print  # pylint: disable=redefined-builtin

from d4v1d.platforms.platform.cmd import CLISessionState, Command
from d4v1d.utils import io


class RemoveGroup(Command):
    """
    Removes a group
    """

    def __init__(self):
        """
        Initializes the command.
        """
        super().__init__('rm group', description='Remove a group from the currently selected platform.')
        self.add_argument('group_name', type=str, help='The name of the group to remove. (e.g. "mygroup")')

    def available(self, state: CLISessionState) -> bool:
        """
        Can this command be used right now?
        """
        return bool(state.platform)

    def completer(self, state: CLISessionState) -> Optional[NestedDict]:
        """
        Custom completer behaviour.
        """
        return { g: None for g in state.platform.groups }

    def execute(self, group_name: str, raw_args: List[str], argv: List[str], state: CLISessionState, *args, **kwargs) -> None:
        """
        Executes the command.

        Args:
            group_name (str): The name of the group to remove.
            raw_args (List[str]): The raw arguments passed to the command.
            argv (List[str]): The extra arguments that weren't parsed.
            state (CLISessionState): The current session state.
        """
        if not state.platform:
            io.e('No platform selected. Use [bold]use[/bold] to select a platform.')
            return
        if group_name not in state.platform.groups:
            io.e(f'Group [bold]{group_name}[/bold] doesn\'t exist.')
            return
        state.platform.rm_group(group_name)
        print(f'[green]Successfully removed group [bold]{group_name}[/bold] from platform [bold]{state.platform.name}[/bold].[/green]')
