"""
Defines the database types for the Tellonym platform.
"""

from enum import Enum


class TellonymDBType(Enum):
    """
    Defines the database types for the Tellonym platform.
    """

    SQLITE = 0
    """SQLite db format"""
