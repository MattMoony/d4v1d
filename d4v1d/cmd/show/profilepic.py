"""
Search the currently loaded platforms for the
profile picture of a specific user.
"""

import shutil
from typing import List, Optional

from image import DrawImage
from rich import print  # pylint: disable=redefined-builtin
from rich.panel import Panel

from d4v1d.platforms.platform.cmd.clisessionstate import CLISessionState
from d4v1d.platforms.platform.cmd.cmd import Command
from d4v1d.platforms.platform.errors import PlatformError
from d4v1d.platforms.platform.info import Info
from d4v1d.utils import io


class ShowProfilePicture(Command):
    """
    Search the currently loaded platforms for the
    profile picture of a specific user.
    """

    def __init__(self):
        """
        Initializes the command.
        """
        super().__init__('show profilepic', description='Show a users profile picture (from the currently enabled platform).')
        self.add_argument('username', type=str, help='The username to search for. (e.g. "d4v1d")')
        self.add_argument('-r', '--refresh', action='store_true', help='Refresh the profile picture from the platform.')
        self.add_argument('-g', '--group', dest='group_name', type=str, help='The group to use for the search.')

    def available(self, state: CLISessionState) -> bool:
        """
        Can it be used rn?
        """
        return bool(state.platform)
    
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
            refresh (Optional[bool]): Refresh the profile picture from the platform?
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
            d: Info[str] = state.platform.get_user_profile_pic(username, refresh=refresh, group=group)
            img: DrawImage = DrawImage.from_file(d.value, 
                                                 size=(
                                                    shutil.get_terminal_size().columns//4, 
                                                    shutil.get_terminal_size().columns//8,
                                                 ))
            print(Panel(d.value, title=f'Profile picture of {username} on {state.platform.name}'))
            img.draw_image()
        except PlatformError as e:
            io.e(f'[bold]{e.__class__.__name__}{":[/bold] "+str(e) if str(e) else "[/bold]"}')
            return
