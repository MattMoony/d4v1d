"""
Search the currently loaded platforms for the
description of a specific user
"""

from typing import List

from rich import print  # pylint: disable=redefined-builtin

from d4v1d.platforms.platform.cmd.clisessionstate import CLISessionState
from d4v1d.platforms.platform.cmd.cmd import Command
from d4v1d.platforms.platform.errors import PlatformError
from d4v1d.platforms.platform.info import Info
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

    def available(self, state: CLISessionState) -> bool:
        """
        Can it be used rn?
        """
        return bool(state.platform)

    def execute(self, username: str, raw_args: List[str], argv: List[str], state: CLISessionState, *args, **kwargs) -> None:
        """
        Executes the command.

        Args:
            username (str): The username to search for.
            args (List[str]): The raw arguments passed to the command.
            state (CLISessionState): The current session state.
        """
        if not state.platform:
            io.e('No platform loaded. Enable one with the [bold]use[/bold] command.')
            return
        try:
            d: Info[str] = state.platform.get_user_description(username)
            print(f'[bold]Description of {username} @ {d.date.isoformat()}:[/bold]\n{d.value}')
        except PlatformError as e:
            io.e(f'[bold]{e.__class__.__name__}{":[/bold] "+str(e) if str(e) else "[/bold]"}')
            return
