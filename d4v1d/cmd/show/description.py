"""
Search the currently loaded platforms for the
description of a specific user
"""

from typing import List, Optional

from prompt_toolkit.completion.nested import NestedDict
from rich import print  # pylint: disable=redefined-builtin
from rich.panel import Panel

from d4v1d.platforms.platform.cmd.clisessionstate import CLISessionState
from d4v1d.platforms.platform.cmd.cmd import Command
from d4v1d.platforms.platform.errors import PlatformError
from d4v1d.platforms.platform.info import Info
from d4v1d.platforms.platform.ptaskopts import PTaskOpts
from d4v1d.platforms.platform.user import User
from d4v1d.utils import io


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
        self.add_argument('username', type=str, help='The username to search for. (e.g. "d4v1d")')
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
            username (Optional[str]): The username to search for.
            refresh (Optional[bool]): Refresh the description from the platform?
            group_name (Optional[str]): The group to use for the search.
        """
        group: Optional[group] = None
        if not username:
            # should NEVER happen
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
            i: Info[User] = state.platform.user(username, opts=PTaskOpts(refresh=refresh, group=group))
            print(Panel(i.value.description, title=f'Description of {username} @ {i.date.isoformat()}'))
        except PlatformError as e:
            io.e(f'[bold]{e.__class__.__name__}{":[/bold] "+str(e) if str(e) else "[/bold]"}')
            return
