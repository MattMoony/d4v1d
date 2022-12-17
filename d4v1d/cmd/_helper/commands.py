"""
Collects all available commands
"""

from d4v1d.cmd.use import Use
from d4v1d.cmd.help import Help
from d4v1d.cmd.exit import Exit
from d4v1d.cmd.show.platforms import ShowPlatforms
from typing import *

CMDS: Dict[str, Any] = {
    'exit': Exit(),
    'show': {
        'platforms': ShowPlatforms(),
    },
    'use': Use(),
}
CMDS['help'] = Help(CMDS)