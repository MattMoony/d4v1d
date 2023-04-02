"""
Removes a bot
"""

from typing import List, Optional

from prompt_toolkit.completion.nested import NestedDict

from d4v1d.platforms.platform.bot.group import Group
from d4v1d.platforms.platform.cmd.clisessionstate import CLISessionState
from d4v1d.platforms.platform.cmd.cmd import Command
from d4v1d.utils import io


class RemoveBot(Command):
    """
    Removes a bot
    """

    def __init__(self) -> None:
        """
        Initializes the command
        """
        super().__init__('rm bot', description='Remove a bot from a group.')
        self.add_argument('group_name', type=str, help='The name of the group from which to remove a bot.')
        self.add_argument('bot_name', type=str, help='The nickname of the bot to remove from the group.')

    def available(self, state: CLISessionState) -> bool:
        """
        Can this command be used right now?
        """
        return bool(state.platform) and bool(state.platform.groups)

    def completer(self, state: CLISessionState) -> Optional[NestedDict]:
        """
        Custom completer behaviour.
        """
        return {
            g: {
                b: None
                for b in _.bots
            }
            for g, _ in state.platform.groups.items()
        }
    
    def execute(self, raw_args: List[str], argv: List[str], state: CLISessionState, *args, 
                group_name: Optional[str] = None, bot_name: Optional[str] = None, **kwargs) -> None:
        """
        Executes the command.

        Args:
            raw_args (List[str]): The raw arguments passed to the command.
            argv (List[str]): The extra arguments that weren't parsed.
            state (CLISessionState): The current session state.
            group_name (Optional[str]): The name of the group from which to remove a bot.
            bot_name (Optional[str]): The name of the bot to remove from the group.
        """
        if not group_name:
            # should NEVER happen
            io.e('Missing group name.')
            return
        if not bot_name:
            # should NEVER happen
            io.e('Missing bot name.')
            return
        if not state.platform:
            io.e('No platform selected. Use [bold]use[/bold] to select a platform.')
            return
        if group_name not in state.platform.groups:
            io.e(f'Group [bold]{group_name}[/bold] doesn\'t exist.')
            return
        group: Group = state.platform.groups[group_name]
        if bot_name not in group.bots:
            io.e(f'Bot [bold]{bot_name}[/bold] not part of group [bold]{group_name}[/bold].')
            return
        group -= group.bots[bot_name]
        io.l(f'Successfully removed bot [bold]{bot_name}[/bold] from group[bold]{group_name}[/bold].')
