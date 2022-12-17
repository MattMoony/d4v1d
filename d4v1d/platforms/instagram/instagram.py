"""
Contains the Instagram class - the interface between
the core and this platform-specific implementation.
"""

from d4v1d.log import log
import d4v1d.config as config
from .db.models import User
from .db import Database, DATABASES
from d4v1d.platforms.platform import Platform
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
        log.debug(f'Initializing database of type "{config.PCONFIG._instagram.db_type}" ...')
        self.db = DATABASES[config.PCONFIG._instagram.db_type]()

    def __del__(self) -> None:
        """
        Do some cleanup, once the platform is unloaded
        in the d4v1d core
        """
        log.debug(f'Cleaning up Instagram ... ')
        del config.PCONFIG._instagram
        del self.db

    def get_user_description(self, username: str) -> str:
        """
        Returns the description of the user with the given username

        Args:
            username (str): The username of the user
        """
        log.debug(f'Check if user ("{username}") is already part of the db')
        user: Optional[User] = self.db.get_user(username)
        if user:
            log.debug(f'"{username}" is already part of the db')
            return user.description
        log.debug(f'"{username}" is not part of the db ... yet')
        # TODO get user info from instagram