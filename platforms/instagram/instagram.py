"""
Contains the Instagram class - the interface between
the core and this platform-specific implementation.
"""

from platforms.platform import Platform
from typing import *

class Instagram(Platform):
    """
    Interface to https://www.instagram.com/
    """

    def __init__(self):
        """
        Creates a new Instagram object
        """
        super().__init__("Instagram", "Wrapper for https://www.instagram.com/")

    def get_user_description(self, username: str) -> str:
        """
        Returns the description of the user with the given username
        """
        # check if user is already part of the db
        pass
