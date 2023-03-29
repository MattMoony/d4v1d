"""
Defines the way databases for the Tellonym
platform should be implemented / what they
should look like. This base class is extended
by all specific database implementations.
"""

from datetime import datetime
from typing import List, Optional

from d4v1d.platforms.tellonym.db.models.tell import TellonymTell
from d4v1d.platforms.tellonym.db.models.user import TellonymUser
from d4v1d.platforms.platform.info import Info


class Database:
    """
    Base class for all Tellonym database interfaces.
    """

    def store_user(self, user: TellonymUser) -> None:
        """
        Stores a user in the database

        Args:
            user (User): The user to store
        """
        raise NotImplementedError()
    
    def store_tells(self, tells: List[Info[TellonymTell]]) -> None:
        """
        Stores a list of tells in the database

        Args:
            tells (List[Info[Tell]]): The tells to store
        """
        raise NotImplementedError()
    
    def update_tells(self, tells: List[Info[TellonymTell]]) -> None:
        """
        Updates a list of tells in the database

        Args:
            tells (List[Info[Tell]]): The tells to update
        """
        raise NotImplementedError()

    def get_user(self, username: Optional[str] = None, id: Optional[int] = None) -> Optional[Info[TellonymUser]]:
        """
        Gets a user from the database.

        Args:
            username (Optional[str]): The username of the user.
            id (Optional[int]): The id of the user.

        Returns:
            Optional[Info[User]]: The user if it exists, None otherwise.
        """
        raise NotImplementedError()
    
    def get_users(self) -> List[Info[TellonymUser]]:
        """
        Get a list of users stored in the DB.

        Returns:
            List[Info[User]]: List of info about users.
        """
        raise NotImplementedError()

    def get_tells(self, user: TellonymUser, _from: datetime, _to: datetime) -> List[Info[TellonymTell]]:
        """
        Gets a list of tells from a user

        Args:
            user (User): The user to get the tells from
            _from (datetime.datetime): The start of the time range
            _to (datetime.datetime): The end of the time range

        Returns:
            List[Info[Tell]]: The tells
        """
        raise NotImplementedError()