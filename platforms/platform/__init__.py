"""
Dummy code for how a platform should
be implemented
"""

from typing import *

class Platform(object):
    """
    Represents a social-media platform
    """
    
    def __init__(self, name: str, desc: str):
        """
        Creates a new platform

        Args:
            name (str): The name of the platform
            desc (str): A description of the platform
        """
        self.name: str = name
        self.desc: str = desc

    def __str__(self) -> str:
        """
        Returns the string representation of the platform

        Returns:
            str: The string representation of the platform
        """
        return self.name
