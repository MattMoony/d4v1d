"""
Dummy code for the platform class.
"""

from typing import *

from d4v1d.log import log
from d4v1d.platforms.platform.bot.group import Group
from d4v1d.platforms.platform.db import Database
from d4v1d.platforms.platform.info import Info


class Platform(object):
    """
    Represents a social-media platform
    """

    name: str
    """The name of the platform"""
    desc: str
    """A description of the platform"""
    groups: Dict[str, Group]
    """The groups of the platform"""
    db: Database
    """The database for storing platform info"""
    cmds: Dict[str, Union["Command", Dict[str, Any]]] = {}
    """Dictionary of custom commands the platform offers - if any."""
    
    def __init__(self, name: str, desc: str, groups: Optional[Dict[str, Group]] = None):
        """
        Creates a new platform

        Args:
            name (str): The name of the platform
            desc (str): A description of the platform
            groups (Optional[Dict[str, Group]]): The groups of the platform
        """
        self.name = name
        self.desc = desc
        self.groups = groups or {}

    def add_group(self, name: str) -> str:
        """
        Create and add a new group with
        the given name.
        """
        raise NotImplementedError()
    
    def rm_group(self, name: str) -> str:
        """
        Removes the group with the given name
        """
        raise NotImplementedError()

    def dumpj(self) -> Dict[str, Any]:
        """
        Returns the platform in save-able dictionary
        format.

        Returns:
            Dict[str, Any]: The platform in save-able dictionary format
        """
        raise NotImplementedError()
    
    @classmethod
    def loadj(cls, data: Dict[str, Any]) -> "Platform":
        """
        Loads the platform from its save-able,
        dictionary format.

        Args:
            data (Dict[str, Any]): The saved format (dumpj)
        
        Returns:
            Platform: The re-constructed platform
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
