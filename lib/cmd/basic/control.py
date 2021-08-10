import lib.cmd
import lib.cmd.bot
from lib import bot
from lib.misc import print_err
from lib.cmd.plugin import D4v1dNubiaPlugin
from nubia import Nubia, command, argument, context
from typing import *

@command
@argument('group_name', name='group', description='Name of the bot group to control', positional=True)
def control(group_name: str) -> None:
    """Control a bot-group"""
    lib.cmd.BOT_GROUP = bot.group(group_name)
    if not lib.cmd.BOT_GROUP:
        print_err('bot-group', 'No group with that name!')
        return
    shell: Nubia = Nubia(
        name=f'd4v1d-{lib.cmd.BOT_GROUP.name}',
        command_pkgs=lib.cmd.bot,
        plugin=D4v1dNubiaPlugin()
    )
    shell.run()
    lib.cmd.BOT_GROUP = None
