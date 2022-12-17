"""
Defines the database types for the Instagram platform.
"""

from enum import Enum
from typing import *

class InstagramDBType(Enum):
    """
    Defines the database types for the Instagram platform.
    """

    SQLITE = 0
    """SQLite db format"""
