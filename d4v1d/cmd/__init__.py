"""
Module responsible for receiving and processing 
commands from the user.
"""

from typing import List, Optional

from d4v1d.utils import io
from d4v1d.cmd._helper import CMDS
from d4v1d.cmd._helper.session import CmdSession


def start(cmds: Optional[List[str]]) -> None:
    """
    Starts handling user input.
    """
    session: CmdSession = CmdSession(CMDS)
    if not cmds:
        session.handle_forever()
    for c in cmds:
        io.l(f'[bold]# {c}[/bold]')
        session.handle(c)
