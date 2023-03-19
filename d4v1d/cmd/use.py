"""
Module for the use command - used 
to switch between platforms
"""

from types import ModuleType
from typing import List, Optional

from prompt_toolkit.completion.nested import NestedDict

from d4v1d import platforms
from d4v1d.platforms.platform.cmd import CLISessionState, Command
from d4v1d.utils import io


class Use(Command):
    """
    The use command
    """

    def __init__(self):
        """
        Initializes the use command
        """
        super().__init__('use', aliases=['switch',], description='Switches between platforms')

    def completer(self, state: CLISessionState) -> Optional[NestedDict]:
        """
        Custom completer behaviour.
        """
        return { n.lower(): None for n in platforms.PLATFORMS.keys() }

    def execute(self, raw_args: List[str], argv: List[str], state: CLISessionState, *args, **kwargs) -> None:
        """
        Executes the use command

        Args:
            raw_args (List[str]): The raw arguments passed to the command.
            argv (List[str]): The extra arguments that weren't parsed.
            state (CLISessionState): The current session state.
        """
        if len(raw_args) == 0:
            if state.platform is not None:
                state.session.remove(state.platform.name)
                del state.platform
                state.platform = None
                io.l('Not using any platform anymore ...')
            return

        platform: str = raw_args.pop(0).lower()
        try:
            p: ModuleType = next(p for n, p in platforms.PLATFORMS.items() if n.lower() == platform)
            if state.platform:
                del state.platform
            state.platform = p.init()
            state.session.extend(state.platform.name, state.platform.cmds)
            io.l(f'Switched to platform [bold]{platform}[/bold]')
        except StopIteration:
            io.e(f'Platform [bold]{platform}[/bold] does not exist')
