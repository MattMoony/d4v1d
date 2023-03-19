"""
Dummy code for the platform class.
"""

from typing import Any, Dict, List, Optional, Union

from d4v1d.platforms.platform.bot.group import Group
from d4v1d.platforms.platform.db import Database
from d4v1d.platforms.platform.groups import Groups
from d4v1d.platforms.platform.info import Info


class Platform:
    """
    Represents a social-media platform
    """

    name: str
    """The name of the platform."""
    desc: str
    """A description of the platform."""
    groups: Groups
    """The groups of the platform."""
    db: Database
    """The database for storing platform info."""
    cmds: Dict[str, Union["Command", Dict[str, Any]]] = {}
    """Dictionary of custom commands the platform offers - if any."""

    def __init__(self, name: str, desc: str, groups: Optional[Groups] = None):
        """
        Creates a new platform

        Args:
            name (str): The name of the platform.
            desc (str): A description of the platform.
            groups (Optional[Groups]): The groups of the platform.
        """
        self.name = name
        self.desc = desc
        self.groups = groups or Groups()
    
    def group(self, name: str) -> Group:
        """
        Create a new group with the given name.

        Returns:
            Group: The new group.
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
    
    def get_cached_usernames(self) -> List[str]:
        """
        Get a list of all usernames whose info has been cached
        locally - so they've been crawled in the past.

        Returns:
            List[str]: The list of usernames of users whose
                information has been collected in the past and
                that are therfore now a part of the DB.
        """
        raise NotImplementedError()

    def get_user_description(self, username: str, refresh: bool = False, group: Optional[Group] = None) -> Info:
        """
        Gets the description of a user

        Args:
            username (str): The username of the user.
            refresh (bool): Whether to force refresh the info.
            group (Optional[Group]): The bot group to use to get the info.

        Returns:
            Info: The description of the user
        """
        raise NotImplementedError()

    def get_user_profile_pic(self, username: str, refresh: bool = False, group: Optional[Group] = None) -> Info:
        """
        Gets the profile picture of a user

        Args:
            username (str): The username of the user.
            refresh (bool): Whether to force refresh the info.
            group (Optional[Group]): The bot group to use to get the info.

        Returns:
            Info: The path to the profile picture of the user
        """
        raise NotImplementedError()

    def get_user_followers(self, username: str, refresh: bool = False, group: Optional[Group] = None) -> Info:
        """
        Gets the followers of a user

        Args:
            username (str): The username of the user.
            refresh (bool): Whether to force refresh the info.
            group (Optional[Group]): The bot group to use to get the info.

        Returns:
            Info: The followers of the user
        """
        raise NotImplementedError()

    def get_user_following(self, username: str, refresh: bool = False, group: Optional[Group] = None) -> Info:
        """
        Gets the following of a user

        Args:
            username (str): The username of the user.
            refresh (bool): Whether to force refresh the info.
            group (Optional[Group]): The bot group to use to get the info.

        Returns:
            Info: The following of the user
        """
        raise NotImplementedError()

    def get_user_number_posts(self, username: str, refresh: bool = False, group: Optional[Group] = None) -> Info:
        """
        Gets the posts of a user

        Args:
            username (str): The username of the user.
            refresh (bool): Whether to force refresh the info.
            group (Optional[Group]): The bot group to use to get the info.

        Returns:
            Info: The posts of the user
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

    def __str__(self) -> str:
        """
        Returns the string representation of the platform

        Returns:
            str: The string representation of the platform
        """
        return self.name
