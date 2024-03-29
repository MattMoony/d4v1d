"""
Removes a group
"""

from typing import List, Optional

from prompt_toolkit.completion.nested import NestedDict

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

    def execute(self, raw_args: List[str], argv: List[str], state: CLISessionState, *args,
                group_name: Optional[str] = None, **kwargs) -> None:
        """
        Executes the command.

        Args:
            raw_args (List[str]): The raw arguments passed to the command.
            argv (List[str]): The extra arguments that weren't parsed.
            state (CLISessionState): The current session state.
            group_name (Optional[str]): The name of the group to remove.
        """
        if not group_name:
            # should NEVER happen
            io.e('Missing group name.')
            return
        if not state.platform:
            io.e('No platform selected. Use [bold]use[/bold] to select a platform.')
            return
        if group_name not in state.platform.groups:
            io.e(f'Group [bold]{group_name}[/bold] doesn\'t exist.')
            return
        state.platform.groups -= group_name
        io.l(f'[Successfully removed group [bold]{group_name}[/bold] from platform [bold]{state.platform.name}[/bold].')
