"""
Class representing a piece of
information relating to a social network.
"""

from datetime import datetime
from typing import Generic, Optional, TypeVar

T = TypeVar('T')

class Info(Generic[T]):
    """
    Represents a piece of information
    """

    value: T
    """The info's value"""
    date: datetime
    """The timestamp of the info"""
    platform: Optional["Platform"]
    """Optionally, the platform the info is from"""

    def __init__(self, value: T, date: datetime, platform: Optional["Platform"] = None):
        """
        Creates a new piece of information

        Args:
            value (Any): The information
            date (datetime): The date of the information
            platform (Optional["Platform"]): The platform
        """
        self.value = value
        self.date = date
        self.platform = platform

    def __str__(self) -> str:
        """
        Returns the string representation of the information

        Returns:
            str: The string representation of the information
        """
        return f'{self.value} ({self.platform if self.platform else ""}@{self.date})'
