"""
Create a new bot for the instagram
social-media platform + add it to a group
already.
"""

from argparse import _ArgumentGroup as ArgumentGroup
from typing import List, Optional, Tuple

from prompt_toolkit.completion.nested import NestedDict

from d4v1d.platforms.instagram.bot.bot import InstagramBot
from d4v1d.platforms.instagram.bot.group import InstagramGroup
from d4v1d.platforms.platform.cmd import CLISessionState, Command
from d4v1d.utils import io


class AddBot(Command):
    """
    Creates a new bot.
    """

    def __init__(self) -> None:
        """
        Initializes the command.
        """
        super().__init__('add bot', description='Create a new bot for the `instagram` platform.')
        self.add_argument('group_name', type=str, help='The name of the group to add the bot to.')
        self.add_argument('--anonymous', action='store_true', help='Whether or not the bot should use the "anonymous" user; i.e. not login.')
        creds: ArgumentGroup = self._parser.add_argument_group('creds')
        creds.add_argument('-u', '--username', type=str, help='The username of the bot.')
        creds.add_argument('-p', '--password', type=str, help='The password of the bot.')
        self.add_argument('--user-agent', type=str, help='The "User-Agent" the bot should use.', default='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
        self.add_argument('-h', '--header', type=str, dest='headers', nargs=2, action='append', help='A header to add to the bot\'s requests. Can be used multiple times.')

    def available(self, state: CLISessionState) -> bool:
        """
        Tell if the command can be used right now.

        Args:
            state (CLISessionState): The current session state.

        Returns:
            bool: True if the command can be used, False otherwise.
        """
        # bot cannot exist without a group
        return bool(state.platform.groups)

    def completer(self, state: CLISessionState) -> Optional[NestedDict]:
        """
        Custom completer behaviour.
        """
        return { g: None for g in state.platform.groups }

    def execute(self, raw_args: List[str], argv: List[str], state: CLISessionState, *args,
                group_name: Optional[str] = None, user_agent: Optional[str] = None,
                anonymous: bool = False, username: Optional[str] = None, password: Optional[str] = None,
                headers: Optional[List[Tuple[str, str]]] = None, **kwargs) -> None:
        """
        Executes the command.

        Args:
            raw_args (List[str]): The raw arguments passed to the command.
            argv (List[str]): The extra arguments that weren't parsed.
            state (CLISessionState): The current session state.
            group_name (Optional[str]): The name of the group to add the bot to.
            user_agent (Optional[str]): The "User-Agent" the bot should use.
            anonymous (bool, optional): Whether or not the bot should use the "anonymous" user; i.e. not login. Defaults to False.
            headers (List[Tuple[str, str]]): The headers to add to the bot's requests.
            username (Optional[str], optional): The username of the bot. Defaults to None.
            password (Optional[str], optional): The password of the bot. Defaults to None.
            headers (Optional[List[Tuple[str, str]]], optional): The headers to add to the bot's requests. Defaults to None.
        """
        if not group_name:
            # shouldn't happen
            io.e('You must provide a group name!')
            return
        if not user_agent:
            # shouldn't happen
            io.e('There must be a user-agent!')
            return
        if not anonymous and not (username and password):
            io.e('You must either set the --anonymous flag or provide username & password!')
            return
        if not state.platform.groups:
            io.e('No groups created yet. Bot cannot exist without a group!')
            return
        if group_name not in state.platform.groups:
            io.e(f'Group "{group_name}" does not exist!')
            return
        group: InstagramGroup = state.platform.groups[group_name]
        bot: InstagramBot = InstagramBot(group, anonymous=anonymous, user_agent=user_agent,
                                         headers=dict(headers or []), creds=(username, password,))
        group.add(bot)
