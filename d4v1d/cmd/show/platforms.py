"""
Show a list of all currently supported
social-media platforms.
"""

from typing import List

from rich import print  # pylint: disable=redefined-builtin
from rich.tree import Tree

from d4v1d.platforms import PLATFORMS
from d4v1d.platforms.platform.cmd import CLISessionState, Command
from d4v1d.utils import io


class ShowPlatforms(Command):
    """
    Show a list of all currently supported
    social-media platforms.
    """

    def __init__(self):
        """
        Initializes the command.
        """
        super().__init__('show platforms', description='Show a list of all currently supported social-media platforms.')

    def execute(self, raw_args: List[str], argv: List[str], state: CLISessionState, *args, **kwargs) -> None:
        """
        Executes the command.
        """
        pl_tree: Tree = Tree(io.fl('Available platforms:'))
        for k in PLATFORMS:
            pl_tree.add(f'[bold]{k}[/bold]')
        print(pl_tree)
