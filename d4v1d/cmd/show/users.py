"""
List the usernames of all users currently
cached locally for the used platform.
"""

from typing import List

from d4v1d.platforms.platform.cmd.clisessionstate import CLISessionState
from d4v1d.platforms.platform.cmd.cmd import Command
from d4v1d.platforms.platform.info import Info
from d4v1d.platforms.platform.user import User
from d4v1d.utils import io


class ShowUsers(Command):
    """
    List the usernames of all users currently
    cached locally for the used platform.
    """

    def __init__(self) -> None:
        """
        Initialize the comamnd.
        """
        super().__init__('show users', description='Show the usernames of all locally cached users (for the current platform).')

    def available(self, state: CLISessionState) -> bool:
        """
        Is the command available rn?

        Args:
            state (CLISessionState): The current prompt session state.

        Returns:
            bool: Whether or not the CMD is currently available.
        """
        return bool(state.platform)

    def execute(self, raw_args: List[str], argv: List[str], state: CLISessionState,
                *args, **kwargs) -> None:
        """
        Execute the command.

        Args:
            raw_args (List[str]): The raw arguments passed to the command.
            argv (List[str]): The arguments passed to the command.
            state (CLISessionState): The current session state.
        """
        users: List[Info[User]] = state.platform.users()
        if not users:
            io.w('No users have been cached for this platform yet!')
            return
        io.l(f'All users, whose info have been cached for "{state.platform.name}":')
        for i in users:
            io.n(f'[bold]{i.value.username}[/bold] @ [italic dim]"{i.date.isoformat()}"[/italic dim]')
