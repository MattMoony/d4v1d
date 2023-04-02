"""
Dummy code for the platform class.
"""

from typing import Any, Dict, List, Optional, Union

from d4v1d.platforms.platform.bot.group import Group
from d4v1d.platforms.platform.db import Database
from d4v1d.platforms.platform.groups import Groups
from d4v1d.platforms.platform.info import Info
from d4v1d.platforms.platform.ptaskopts import PTaskOpts
from d4v1d.platforms.platform.user import User


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

    def __init__(self, name: str, desc: str, groups: Optional[Groups] = None) -> None:
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

    def user(self, username: str, opts: PTaskOpts = PTaskOpts()) -> Info[User]:
        """
        Get the user with the given username from
        the platform.

        Args:
            username (str): The user's username.
            opts (PTaskOpts): The options for the task.

        Returns:
            Info[User]: The user info + the timestamp, when it was retrieved.

        Raises:
            KeyError: In case no user with this ``username`` was found.
        """
        raise NotImplementedError()

    def users(self) -> List[Info[User]]:
        """
        Return a list of all locally cached users and
        their info.

        Returns:
            List[Info[User]: List of user information.
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

    def __str__(self) -> str:
        """
        Returns the string representation of the platform

        Returns:
            str: The string representation of the platform
        """
        return self.name

    def __getitem__(self, username: str) -> User:
        """
        Get information about the user with the given 
        username; will **always** try to get the user 
        information from the local cache before scraping it.

        To get new, refreshed user information use
        the ``.user()`` method directly as it works
        for such requirements.

        Args:
            username (str): The user's username.

        Returns:
            User: The info about the user matching the username.

        Raises:
            KeyError: In case no user with the given
                username exists.
        """
        raise NotImplementedError()
