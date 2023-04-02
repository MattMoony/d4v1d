"""
Contains the definition of the Bot class,
i.e. an automated user / anonymous browser of 
the target social-media platform.
"""

from typing import Dict, Any

class Bot:
    """
    Template bot class - template automated user.
    """

    nickname: str
    """The nickname of the bot"""
    group: "Group"
    """The group the bot belongs to"""
    anonymous: bool
    """Whether or not the bot is an authenticated user"""
    requests: int
    """The number of requests the bot has made"""

    def __init__(self, nickname: str, group: "Group", anonymous: bool):
        """
        Creates a new Bot object

        Args:
            group (Group): The group the bot belongs to
            anonymous (bool): Whether the bot should be anonymous
        """
        self.nickname = nickname
        self.group = group
        self.anonymous = anonymous
        self.requests = 0

    def dumpj(self) -> Dict[str, Any]:
        """
        Returns the bot in saveable format.

        Returns:
            Dict[str, Any]: The bot in saveable dictionary format
        """
        raise NotImplementedError()

    def __str__(self) -> str:
        return f'"{self.nickname}"@No Platform ()'

    def __repr__(self) -> str:
        return f'<{self}>'

    @classmethod
    def loadj(cls, data: Dict[str, Any], group: "Group") -> "Bot":
        """
        Loads the bot from its saveable,
        dictionary format.

        Args:
            data (Dict[str, Any]): The saved format (dumpj)
        
        Returns:
            Platform: The re-constructed bot
        """
        raise NotImplementedError()
