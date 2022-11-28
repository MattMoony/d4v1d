"""
Collects all available commands
"""

from cmd.use import Use
from cmd.help import Help
from cmd.exit import Exit
from cmd.show.platforms import ShowPlatforms
from typing import *

CMDS: Dict[str, Any] = {
    'exit': Exit(),
    'show': {
        'platforms': ShowPlatforms(),
    },
    'use': Use(),
}
CMDS['help'] = Help(CMDS)