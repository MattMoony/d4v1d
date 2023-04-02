"""
Show a list of all bots defined for the 
current platform
"""

from typing import List, Optional

from rich import print  # pylint: disable=redefined-builtin
from rich.tree import Tree

from d4v1d.platforms.platform.cmd import CLISessionState, Command
from d4v1d.utils import io


class ShowBots(Command):
    """
    Show a list of all bots defined for the 
    current platform
    """

    def __init__(self):
        """
        Initializes the command.
        """
        super().__init__('show bots', description='Show a list of all bots defined for the current platform.')
        self.add_argument('group_name', type=str, help='The group to show the bots of. If not specified, all groups will be shown.', default=None, nargs='?')

    def available(self, state: CLISessionState) -> bool:
        """
        Can it be used rn?
        """
        return bool(state.platform) and bool(state.platform.groups)

    def execute(self, raw_args: List[str], argv: List[str], state: CLISessionState, *args,
                group_name: Optional[str] = None, **kwargs) -> None:
        """
        Executes the command.
        """
        if not state.platform:
            io.e('No platform selected. Use [bold]use[/bold] to select a platform.')
            return
        if not state.platform.groups:
            io.w(f'No groups defined for platform [bold]{state.platform.name}[/bold].')
            return
        tr: Tree = Tree(io.fl(f'Bots defined for [italic]{state.platform.name}[/italic]:'))
        for g in state.platform.groups.values():
            if group_name and g.name != group_name:
                continue
            subtr: Tree = tr.add(f'[bold]{g.name} ({len(g.bots)} bots)[/bold]')
            for b in g.bots.values():
                subtr.add(f'[bold]{b.nickname}[/bold] ({"anonymous" if b.anonymous else b.username})')
        print(tr)
