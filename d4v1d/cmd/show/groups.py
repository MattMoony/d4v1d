"""
Show a list of all groups defined for the 
current platform
"""

from rich import print
from rich.tree import Tree
from d4v1d.utils import io
from d4v1d.platforms import PLATFORMS
from d4v1d.platforms.platform.cmd import Command, CLISessionState
from typing import *

class ShowGroups(Command):
    """
    Show a list of all groups defined for the 
    current platform
    """

    def __init__(self):
        """
        Initializes the command.
        """
        super().__init__('show groups', description='Show a list of all groups defined for the current platform.')

    def execute(self, args: List[str], state: CLISessionState) -> None:
        """
        Executes the command.
        """
        if not state.platform:
            io.e('No platform selected. Use [bold]use[/bold] to select a platform.')
            return
        if not state.platform.groups:
            io.w(f'No groups defined for platform [bold]{state.platform.name}[/bold].')
            return
        tr: Tree = Tree('[bold grey53][*][/bold grey53] Available platforms:')
        for g in state.platform.groups:
            tr.add(f'[bold]{g.name} ({len(g.bots)} bots)[/bold]')
        print(tr)