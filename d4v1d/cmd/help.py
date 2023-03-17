"""
Module for the help command
"""

from typing import *

from prompt_toolkit.completion.nested import NestedDict
from rich import print
from rich.tree import Tree

from d4v1d.platforms.platform.cmd import CLISessionState, Command


class Help(Command):
    """
    The help command
    """

    def __init__(self):
        """
        Initializes the help command
        """
        super().__init__('help', aliases=['?',], description='Shows this help message')

    def __build_tree(self, cmds: Dict[str, Any], tree: Tree, state: CLISessionState) -> None:
        """
        Builds a tree of commands from the specified dictionary

        Args:
            cmds (Dict[str, Any]): The dictionary of commands
            tree (Tree): The tree to build
            state (CLISessionState): The current cli session state
        """
        done: List[Command] = []
        for k, v in cmds.items():
            if isinstance(v, Command) and v.available(state) and v not in done:
                tree.add(f'[bold]{v.name}[/bold]: {v.description}')
                done.append(v)
            elif isinstance(v, dict):
                t: Tree = Tree(k)
                self.__build_tree(v, t, state)
                if t.children:
                    tree.add(t)

    def completer(self, state: CLISessionState) -> Optional[NestedDict]:
        """
        Custom completer behaviour.
        """
        return state.session.compl_dict

    def execute(self, args: List[str], state: CLISessionState) -> None:
        """
        Executes the help command
        """
        cmds: Dict[str, Union[Command, Dict[str, Any]]] = {}
        for v in state.session.cmds.values():
            state.session.deep_merge(cmds, v)

        if len(args) == 0:
            # seems a little redunant, but keeps aliases
            # out of the top-level overview, at least ...
            cmd_tree: Tree = Tree('[bold grey53][*][/bold grey53] Available commands:')
            self.__build_tree(cmds, cmd_tree, state)
            print(cmd_tree)
        else:
            try:
                c, _ = state.session.parse(args)
                if isinstance(c, Command):
                    print(f'[bold grey53][*][/bold grey53] [bold]{c.name}[/bold]: {c.description}')
                    if len(c.aliases) > 0:
                        print(f'    └── Aliases: [bold]{", ".join(c.aliases)}[/bold]')
                else:
                    cmd_tree: Tree = Tree('[bold grey53][*][/bold grey53] Available sub-commands:')
                    self.__build_tree(c, cmd_tree, state)
                    print(cmd_tree)
            except KeyError:
                print(f'[bold red][-][/bold red] Unknown command: [italic]{" ".join(args)}[/italic]. Enter [bold]help[/bold] to see all available commands ...')