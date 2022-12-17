"""
Dummy code for the platform class.
"""

from d4v1d.platforms.platform.info import Info
from typing import *

class Platform(object):
    """
    Represents a social-media platform
    """
    
    def __init__(self, name: str, desc: str):
        """
        Creates a new platform

        Args:
            name (str): The name of the platform
            desc (str): A description of the platform
        """
        self.name: str = name
        self.desc: str = desc

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
