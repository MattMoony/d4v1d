"""
Defines the way databases for the Instagram
platform should be implemented / what they
should look like. This base class is extended
by all specific database implementations.
"""

from datetime import datetime
from typing import List, Optional

from d4v1d.platforms.instagram.db.models.location import InstagramLocation
from d4v1d.platforms.instagram.db.models.post import InstagramPost
from d4v1d.platforms.instagram.db.models.user import InstagramUser
from d4v1d.platforms.platform.info import Info


class Database:
    """
    Base class for all Instagram database interfaces.
    """

    def store_user(self, user: InstagramUser) -> None:
        """
        Stores a user in the database

        Args:
            user (User): The user to store
        """
        raise NotImplementedError()
    
    def store_posts(self, posts: List[Info[InstagramPost]]) -> None:
        """
        Stores a list of posts in the database

        Args:
            posts (List[Info[Post]]): The posts to store
        """
        raise NotImplementedError()
    
    def store_location(self, location: InstagramLocation) -> None:
        """
        Stores a location in the database

        Args:
            location (Location): The location to store
        """
        raise NotImplementedError()

    def get_user(self, username: Optional[str] = None, id: Optional[int] = None) -> Optional[Info[InstagramUser]]:
        """
        Gets a user from the database.

        Args:
            username (Optional[str]): The username of the user.
            id (Optional[int]): The id of the user.

        Returns:
            Optional[Info[User]]: The user if it exists, None otherwise.
        """
        raise NotImplementedError()
    
    def get_users(self) -> List[Info[InstagramUser]]:
        """
        Get a list of users stored in the DB.

        Returns:
            List[Info[User]]: List of info about users.
        """
        raise NotImplementedError()

    def get_posts(self, user: InstagramUser, _from: datetime, _to: datetime) -> List[Info[InstagramPost]]:
        """
        Gets a list of posts from a user

        Args:
            user (User): The user to get the posts from
            _from (datetime.datetime): The start of the time range
            _to (datetime.datetime): The end of the time range

        Returns:
            List[Info[Post]]: The posts
        """
        raise NotImplementedError()
    
    def get_location(self, id: int) -> Optional[InstagramLocation]:
        """
        Gets a location from the database

        Args:
            id (int): The id of the location

        Returns:
            Optional[InstagramLocation]: The location if it exists, None otherwise.
        """
        raise NotImplementedError()
