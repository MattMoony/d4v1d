"""
Collects all available commands
"""

from d4v1d.cmd.use import Use
from d4v1d.cmd.help import Help
from d4v1d.cmd.exit import Exit
from d4v1d.cmd.add.group import AddGroup
from d4v1d.cmd.rm.group import RemoveGroup
from d4v1d.cmd.show.groups import ShowGroups
from d4v1d.cmd.show.platforms import ShowPlatforms
from d4v1d.cmd.show.description import ShowDescription
from typing import *

CMDS: Dict[str, Any] = {
    'add': {
        'group': AddGroup(),
    },
    'exit': Exit(),
    'show': {
        'description': ShowDescription(),
        'groups': ShowGroups(),
        'platforms': ShowPlatforms(),
    },
    'rm': {
        'group': RemoveGroup(),
    },
    'use': Use(),
}
CMDS['help'] = Help(CMDS)