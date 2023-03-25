"""
Turn debug logging on/off.
"""

import logging
from typing import List, Optional

from prompt_toolkit.completion.nested import NestedDict

from d4v1d import config
from d4v1d.platforms.platform.cmd.clisessionstate import CLISessionState
from d4v1d.platforms.platform.cmd.cmd import Command
from d4v1d.utils import io


class DebugLog(Command):
    """
    Turn debug logging on/off.
    """

    def __init__(self):
        """
        Initializes the command.
        """
        super().__init__('.debug log', description='Turn debug logging on/off.')
        self.add_argument('on_off', type=str, help='Turn debug logging on/off.')

    def completer(self, state: CLISessionState) -> Optional[NestedDict]:
        """
        Auto-complete the command.
        """
        return {
            'on': None,
            'off': None,
        }

    def execute(self, raw_args: List[str], argv: List[str], state: CLISessionState, *args, 
                on_off: Optional[str] = None, **kwargs) -> None:
        """
        Executes the command.
        """
        if not on_off:
            # should not happen
            io.e('No on/off value provided.')
            return
        config.LOG_LEVEL = 'DEBUG' if on_off.lower() == 'on' else 'INFO'
        logging.getLogger(config.LOG_NAME).setLevel(config.LOG_LEVEL)
        io.l(f'Debug logging turned [bold]{on_off}[/bold].')
