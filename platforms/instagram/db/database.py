"""
Defines the way databases for the Instagram
platform should be implemented / what they
should look like. This base class is extended
by all specific database implementations.
"""

from platforms.instagram.db.models import User
from typing import *

class Database(object):
    """
    Base class for all Instagram database interfaces.
    """
    
    def store_user(self, user: User) -> None:
        """
        Stores a user in the database

        Args:
            user (User): The user to store
        """
        raise NotImplementedError()

    def get_user(self, username: str) -> Optional[User]:
        """
        Gets a user from the database

        Args:
            username (str): The username of the user

        Returns:
            Optional[User]: The user if it exists, None otherwise
        """
        raise NotImplementedError()