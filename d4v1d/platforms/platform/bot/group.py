"""
Contains the definition of the Group class,
i.e. a collection of Bot objects, which means
a collection of automated users / anonymous
browsers.
"""

from typing import Any, Dict, List, Optional

from d4v1d.platforms.platform.bot.bot import Bot


class Group:
    """
    Template group class - template collection of bots.
    """

    name: str
    """The name of the group"""
    bots: List[Bot]
    """The bots in the group"""

    def __init__(self, name: str, bots: Optional[List[Bot]] = None):
        """
        Initialize the group with a name and an 
        optional list of bots.

        Args:
            name (str): The name of the group
            bots (Optional[List[Bot]]): The bots in the group
        """
        self.name = name
        self.bots = bots or []

    def add(self, bot: Bot):
        """
        Adds a bot to the group

        Args:
            bot (Bot): The bot to add
        """
        self.bots.append(bot)

    def remove(self, bot: Bot):
        """
        Removes a bot from the group

        Args:
            bot (Bot): The bot to remove
        """
        self.bots.remove(bot)

    def dumpj(self) -> Dict[str, Any]:
        """
        Returns the group in saveable format.

        Returns:
            Dict[str, Any]: The group in saveable dictionary format
        """
        raise NotImplementedError()

    @classmethod
    def loadj(cls, data: Dict[str, Any]) -> "Group":
        """
        Loads the group from its saveable,
        dictionary format.

        Args:
            data (Dict[str, Any]): The saved format (dumpj)
        
        Returns:
            Platform: The re-constructed group
        """
        raise NotImplementedError()
