"""
Dummy code for the platform class.
"""

from d4v1d.platforms.platform.bot.group import Group
from d4v1d.platforms.platform.info import Info
from typing import *

class Platform(object):
    """
    Represents a social-media platform
    """

    name: str
    """The name of the platform"""
    desc: str
    """A description of the platform"""
    groups: List[Group]
    """The groups of the platform"""
    
    def __init__(self, name: str, desc: str, groups: Optional[List[Group]] = None):
        """
        Creates a new platform

        Args:
            name (str): The name of the platform
            desc (str): A description of the platform
            groups (Optional[List[Group]]): The groups of the platform
        """
        self.name = name
        self.desc = desc
        self.groups = groups or []

    def add_group(self, name: str) -> str:
        """
        Create and add a new group with
        the given name.
        """
        raise NotImplementedError()

    @classmethod
    def get_user_description(cls, username: str) -> Info:
        """
        Gets the description of a user

        Args:
            username (str): The username of the user

        Returns:
            Info: The description of the user
        """
        raise NotImplementedError()

    @classmethod
    def get_user_profile_pic(cls, username: str) -> Info:
        """
        Gets the profile picture of a user

        Args:
            username (str): The username of the user

        Returns:
            Info: The path to the profile picture of the user
        """
        raise NotImplementedError()

    @classmethod
    def get_user_followers(cls, username: str) -> Info:
        """
        Gets the followers of a user

        Args:
            username (str): The username of the user

        Returns:
            Info: The followers of the user
        """
        raise NotImplementedError()

    @classmethod
    def get_user_following(cls, username: str) -> Info:
        """
        Gets the following of a user

        Args:
            username (str): The username of the user

        Returns:
            Info: The following of the user
        """
        raise NotImplementedError()

    @classmethod
    def get_user_posts(cls, username: str) -> Info:
        """
        Gets the posts of a user

        Args:
            username (str): The username of the user

        Returns:
            Info: The posts of the user
        """
        raise NotImplementedError()

    def __str__(self) -> str:
        """
        Returns the string representation of the platform

        Returns:
            str: The string representation of the platform
        """
        return self.name
