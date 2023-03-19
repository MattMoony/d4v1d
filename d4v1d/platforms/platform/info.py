"""
Class representing a piece of
information relating to a social network.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Generic, Optional, TypeVar

T = TypeVar('T')

@dataclass
class Info(Generic[T]):
    """
    Represents a piece of information
    """

    value: T
    """The info's value"""
    date: datetime
    """The timestamp of the info"""
    platform: Optional["Platform"] = None
    """Optionally, the platform the info is from"""

    def __str__(self) -> str:
        """
        Returns the string representation of the information

        Returns:
            str: The string representation of the information
        """
        return f'{self.value} ({self.platform if self.platform else ""}@{self.date})'
