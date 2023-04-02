"""
Show all posts a user has made on
Instagram.
"""

from typing import List, Optional

from prompt_toolkit.completion.nested import NestedDict

from d4v1d.platforms.instagram.db.models.post import InstagramPost
from d4v1d.platforms.platform.cmd.clisessionstate import CLISessionState
from d4v1d.platforms.platform.cmd.cmd import Command
from d4v1d.platforms.platform.errors import PlatformError
from d4v1d.platforms.platform.info import Info
from d4v1d.platforms.platform.ptaskopts import PTaskOpts
from d4v1d.utils import io


class ShowPosts(Command):
    """
    Show all posts a user has made on
    Instagram.
    """

    def __init__(self) -> None:
        """
        Initialize the command.
        """
        super().__init__('show posts', description='Show all posts a user has made on Instagram.')
        self.add_argument('username', help='The username of the user.')
        self.add_argument('-d', '--download', action='store_true', help='Download the posts.')
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
                username: Optional[str] = None, download: bool = False, refresh: bool = False,
                group_name: Optional[str] = None, **kwargs) -> None:
        """
        Executes the command.

        Args:
            raw_args (List[str]): The raw arguments passed to the command.
            argv (List[str]): The arguments passed to the command.
            state (CLISessionState): The current session state.
            username (Optional[str]): The username of the user.
            download (bool): Whether to download the posts.
            refresh (bool): Whether to refresh the posts.
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
            posts: List[Info[InstagramPost]] = state.platform.posts(username, download=download, opts=PTaskOpts(refresh=refresh, group=group))
            if not posts:
                io.w(f'No posts found for [bold]{username}[/bold] on Instagram. Perhaps the account is private?')
                return
            io.l(f'Found a total of {len(posts)} post{"s" if len(posts) > 1 else ""} made by [bold]{username}[/bold] on Instagram:')
            for i in posts:
                io.n(f'{i.value.short_code}: [bold]{i.value.caption.replace(chr(0xa), " ") if len(i.value.caption) <= 32 else i.value.caption[:32].replace(chr(0xa), " ") + " ..."}[/bold] (from "{i.value.taken_at.isoformat()}") @ [italic dim]"{i.date.isoformat()}"[/italic dim]')
        except PlatformError as e:
            io.e(f'[bold]{e.__class__.__name__}{":[/bold] "+str(e) if str(e) else "[/bold]"}')
            return
