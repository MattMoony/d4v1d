"""
Responsible for storing some information
about the state of the CLI session
"""

from d4v1d.platforms.platform import Platform
from typing import *

class CLISessionState(object):
    """
    Stores some data about the current 
    state of the CLI
    """

    session: "CmdSession"
    """The prompt session taking commands from the user."""
    platform: Optional[Platform] = None
    """The currently activated platform, if any."""

    def __init__(self, session: "CmdSession"):
        """
        Initializes the session state

        Args:
            session (CmdSession): The prompt session
        """
        self.session = session
