"""
Collects all available commands
"""

from typing import Any, Dict

from d4v1d.cmd.add.group import AddGroup
from d4v1d.cmd.debug.bot import DebugBot
from d4v1d.cmd.debug.log import DebugLog
from d4v1d.cmd.exit import Exit
from d4v1d.cmd.help import Help
from d4v1d.cmd.rm.bot import RemoveBot
from d4v1d.cmd.rm.group import RemoveGroup
from d4v1d.cmd.show.bots import ShowBots
from d4v1d.cmd.show.description import ShowDescription
from d4v1d.cmd.show.groups import ShowGroups
from d4v1d.cmd.show.numberposts import ShowNumberPosts
from d4v1d.cmd.show.platforms import ShowPlatforms
from d4v1d.cmd.show.profilepic import ShowProfilePicture
from d4v1d.cmd.show.users import ShowUsers
from d4v1d.cmd.use import Use

CMDS: Dict[str, Any] = {
    '.debug': {
        'bot': DebugBot(),
        'log': DebugLog(),
    },
    'add': {
        'group': AddGroup(),
    },
    'exit': Exit(),
    'help': Help(),
    'show': {
        '#posts': ShowNumberPosts(),
        'bots': ShowBots(),
        'description': ShowDescription(),
        'groups': ShowGroups(),
        'platforms': ShowPlatforms(),
        'profilepic': ShowProfilePicture(),
        'users': ShowUsers(),
    },
    'rm': {
        'bot': RemoveBot(),
        'group': RemoveGroup(),
    },
    'use': Use(),
}
"""All standard commands."""
