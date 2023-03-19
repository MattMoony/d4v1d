"""
Defines the way databases for the Instagram
platform should be implemented / what they
should look like. This base class is extended
by all specific database implementations.
"""

from typing import List, Optional

from d4v1d.platforms.instagram.db.models import User
from d4v1d.platforms.platform.info import Info


class Database:
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

    def get_user(self, username: str) -> Optional[Info[User]]:
        """
        Gets a user from the database

        Args:
            username (str): The username of the user

        Returns:
            Optional[Info[User]]: The user if it exists, None otherwise
        """
        raise NotImplementedError()
    
    def get_users(self) -> List[Info[User]]:
        """
        Get a list of users stored in the DB.

        Returns:
            List[Info[User]]: List of info about users.
        """
        raise NotImplementedError()
