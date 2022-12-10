"""
Contains the Instagram class - the interface between
the core and this platform-specific implementation.
"""

import config
from .db import Database
from platforms.platform import Platform
from typing import *

class Instagram(Platform):
    """
    Interface to https://www.instagram.com/
    """

    db: Database
    """The database for instagram info"""

    def __init__(self):
        """
        Creates a new Instagram object
        """
        super().__init__("Instagram", "Wrapper for https://www.instagram.com/")

    def __del__(self) -> None:
        """
        Do some cleanup, once the platform is unloaded
        in the d4v1d core
        """
        del config.PCONFIG._instagram

    def get_user_description(self, username: str) -> str:
        """
        Returns the description of the user with the given username

        Args:
            username (str): The username of the user
        """
        # check if user is already part of the db
        pass
