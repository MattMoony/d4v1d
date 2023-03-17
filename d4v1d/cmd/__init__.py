"""
Module responsible for receiving and processing 
commands from the user.
"""

from d4v1d.cmd._helper import CMDS
from d4v1d.cmd._helper.session import CmdSession

def start() -> None:
    """
    Starts handling user input.
    """
    session: CmdSession = CmdSession(CMDS)
    session.handle_forever()
