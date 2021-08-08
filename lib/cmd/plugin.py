import lib.cmd.basic
from lib.bot import BotGroup
from pygments.token import Token
from nubia import PluginInterface, context
from typing import *

class D4v1dNubiaPlugin(PluginInterface):
    """Customizes the Nubia shell"""

    def get_prompt_tokens(self, context: context.Context) -> List[Tuple[Any, str]]:
        """Returns the prompt text for the shell"""
        return [
            (Token.Username, 'd4v1d'),
            (Token.Colon, f'|{lib.cmd.BOT_GROUP.name}' if lib.cmd.BOT_GROUP else ''),
            (Token.Pound, '> '),
        ]