"""
Class representing a piece of
information relating to a social network.
"""

from datetime import datetime
from . import Platform
from typing import *

class Info(object):
    """
    Represents a piece of information
    """
    def __init__(self, value: Any, date: datetime, platform: Platform):
        """
        Creates a new piece of information

        Args:
            value (Any): The information
            date (datetime): The date of the information
            platform (Platform): The platform
        """
        self.value: Any = value
        self.date: datetime = date
        self.platform: Platform = platform

    def __str__(self) -> str:
        """
        Returns the string representation of the information

        Returns:
            str: The string representation of the information
        """
        return f'{self.value} ({self.platform}@{self.date})'
