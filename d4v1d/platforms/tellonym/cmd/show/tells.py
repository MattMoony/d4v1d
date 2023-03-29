"""
Show all tells a user has made on
Tellonym.
"""

from typing import List, Optional

from prompt_toolkit.completion.nested import NestedDict

from d4v1d.platforms.tellonym.db.models.tell import TellonymTell 
from d4v1d.platforms.platform.cmd.clisessionstate import CLISessionState
from d4v1d.platforms.platform.cmd.cmd import Command
from d4v1d.platforms.platform.errors import PlatformError
from d4v1d.platforms.platform.info import Info
from d4v1d.utils import io


class ShowTells(Command):
    """
    Show all tells a user has made on
    Tellonym.
    """

    def __init__(self) -> None:
        """
        Initialize the command.
        """
        super().__init__('show tells', description='Show all tells a user has made on Tellonym.')
        self.add_argument('username', help='The username of the user.')
        self.add_argument('-r', '--refresh', action='store_true', help='Refresh the description from the platform.')
        self.add_argument('-g', '--group', dest='group_name', type=str, help='The group to use for the search.')

    def available(self, state: CLISessionState) -> bool:
        """
        Can it be used rn?
        """
        return bool(state.platform)
    
    def completer(self, state: CLISessionState) -> Optional[NestedDict]:
        """
        Custom command auto-completion.
        """
        return { i.value.username: None for i in state.platform.users() }
    
    def execute(self, raw_args: List[str], argv: List[str], state: CLISessionState, *args,
                username: Optional[str] = None, refresh: bool = False,
                group_name: Optional[str] = None, **kwargs) -> None:
        """
        Executes the command.

        Args:
            raw_args (List[str]): The raw arguments passed to the command.
            argv (List[str]): The arguments passed to the command.
            state (CLISessionState): The current session state.
            username (Optional[str]): The username of the user.
            refresh (bool): Whether to refresh the tells.
            group_name (Optional[str]): The group to use for the search.
        """
        group: Optional[group] = None
        if not username:
            # should not happen
            io.e('No username provided.')
            return
        if not state.platform:
            io.e('No platform loaded. Enable one with the [bold]use[/bold] command.')
            return
        if group_name:
            if group_name not in state.platform.groups:
                io.e(f'Group "{group_name}" is unknown.')
                return
            group = state.platform.groups[group_name]
        try:
            tells: List[Info[TellonymTell]] = state.platform.tells(username, refresh=refresh, group=group)
            if not tells:
                io.w(f'No tells found for [bold]{username}[/bold] on Tellonym.')
                return
            io.l(f'Found a total of {len(tells)} tell{"s" if len(tells) > 1 else ""} made by [bold]{username}[/bold] on Tellonym:')
            for i in tells:
                io.n(f'{i.value.id}: [bold]{i.value.tell}[/bold] (from "{i.value.createdAt}") @ [italic dim]"{i.date.isoformat()}"[/italic dim]')
        except PlatformError as e:
            io.e(f'[bold]{e.__class__.__name__}{":[/bold] "+str(e) if str(e) else "[/bold]"}')
            return
