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
    platform: Optional[Platform] = None