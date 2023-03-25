"""
Drop into an interactive debugging session
with a bot.
"""

from typing import List, Optional

from prompt_toolkit.completion.nested import NestedDict

from d4v1d.platforms.platform.bot.group import Group
from d4v1d.platforms.platform.cmd.clisessionstate import CLISessionState
from d4v1d.platforms.platform.cmd.cmd import Command
from d4v1d.utils import io


class DebugBot(Command):
    """
    Drop into an interactive debugging session
    with a bot.
    """

    def __init__(self):
        """
        Initializes the command.
        """
        super().__init__('.debug bot', description='Drop into an interactive debugging session with a bot.')
        self.add_argument('group_name', type=str, help='The group the bot is in.')
        self.add_argument('bot_nick', type=str, help='The bot to debug.')

    def available(self, state: CLISessionState) -> bool:
        """
        Checks if the command is available.
        """
        return bool(state.platform) and bool(state.platform.groups) and any(bool(g.bots) for g in state.platform.groups.values())

    def completer(self, state: CLISessionState) -> Optional[NestedDict]:
        """
        Auto-complete the command.
        """
        return {
            g.name: {
                b.nickname: None
                for b in g.bots.values()
            }
            for g in state.platform.groups.values()
        }

    def execute(self, raw_args: List[str], argv: List[str], state: CLISessionState, *args,
                group_name: Optional[str] = None, bot_nick: Optional[str] = None, **kwargs) -> None:
        """
        Executes the command.
        """
        if not group_name:
            # should not happen
            io.e('No group name provided.')
            return
        if not bot_nick:
            # should not happen
            io.e('No bot nick provided.')
            return
        if group_name not in state.platform.groups:
            io.e(f'Group [bold]{group_name}[/bold] not found.')
            return
        group: Group = state.platform.groups[group_name]
        if bot_nick not in group.bots:
            io.e(f'Bot [bold]{bot_nick}[/bold] not found in group "{group_name}".')
            return
        if not hasattr(group.bots[bot_nick], 'debug'):
            io.e(f'Bot [bold]{bot_nick}[/bold] does not support debugging.')
            return
        group.bots[bot_nick].debug()
        io.l(f'Bot [bold]{bot_nick}[/bold] debug session ended.')
