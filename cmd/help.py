"""
Module for the help command
"""

from rich import print
from rich.tree import Tree
from cmd.cmd import Command
from cmd._helper.clisessionstate import CLISessionState
from typing import *

class Help(Command):
    """
    The help command
    """

    def __init__(self, cmds: Dict[str, Any]):
        """
        Initializes the help command

        Args:
            cmds (Dict[str, Any]): The dictionary of commands
        """
        super().__init__('help', aliases=['?',], description='Shows this help message')
        self.cmds: Dict[str, Any] = cmds

    def __build_tree(self, cmds: Dict[str, Any], tree: Tree) -> None:
        """
        Builds a tree of commands from the specified dictionary

        Args:
            cmds (Dict[str, Any]): The dictionary of commands
            tree (Tree): The tree to build
        """
        done: List[Command] = []
        for k, v in cmds.items():
            if isinstance(v, Command) and v not in done:
                tree.add(f'[bold]{v.name}[/bold]: {v.description}')
                done.append(v)
            elif isinstance(v, dict):
                t: Tree = tree.add(k)
                self.__build_tree(v, t)

    def execute(self, args: List[str], state: CLISessionState) -> None:
        """
        Executes the help command
        """
        if len(args) == 0:
            cmd_tree: Tree = Tree('[bold grey53][*][/bold grey53] Available commands:')
            self.__build_tree(self.cmds, cmd_tree)
            print(cmd_tree)
        else:
            cmd: str = args.pop(0)
            if cmd in self.cmds:
                c: Command = self.cmds[cmd]
                if isinstance(c, Command):
                    print(f'[bold grey53][*][/bold grey53] [bold]{c.name}[/bold]: {c.description}')
                    if len(c.aliases) > 0:
                        print(f'    └── Aliases: [bold]{", ".join(c.aliases)}[/bold]')
                else:
                    # TODO: Add support for subcommands
                    print(f'[bold grey53][*][/bold grey53] [italic]TODO[/italic]')
            else:
                print(f'[bold red][-][/bold red] Unknown command: [italic]{cmd}[/italic]. Enter [bold]help[/bold] to see all available commands ...')