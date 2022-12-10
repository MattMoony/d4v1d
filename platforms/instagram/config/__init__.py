"""
Contains configuration specific to the Instagram platform.
"""

from .dbtype import InstagramDBType
from typing import *

class InstagramConfig(object):
    """
    Configuration class for Instagram.
    """

    db_type: InstagramDBType
    """The type of database to use"""
    headers: Dict[str, str]
    """The headers to use for requests"""
    user_agents: List[str]
    """The user agents to use for requests"""
