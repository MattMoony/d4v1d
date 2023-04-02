"""
Contains the definition of the Group class,
i.e. a collection of Bot objects, which means
a collection of automated users / anonymous
browsers.
"""

from typing import Any, Dict, Optional

from d4v1d.platforms.platform.bot.bot import Bot


class Group:
    """
    Template group class - template collection of bots.
    """

    name: str
    """The name of the group"""
    bots: Dict[str, Bot]
    """The bots in the group"""

    def __init__(self, name: str, bots: Optional[Dict[str, Bot]] = None):
        """
        Initialize the group with a name and an 
        optional list of bots.

        Args:
            name (str): The name of the group.
            bots (Optional[Dict[str, Bot]]): The bots in the group.
        """
        self.name = name
        self.bots = bots or {}

    def add(self, bot: Bot) -> None:
        """
        Adds a bot to the group.

        Args:
            bot (Bot): The bot to add.

        Raises:
            ValueError: If the bot (or a bot with the same nickname) 
                already exists in the group.
        """
        if bot.nickname in self.bots:
            raise ValueError(f'Bot with nickname {bot.nickname} already exists in group {self.name}!')
        self.bots[bot.nickname] = bot

    def remove(self, bot: Bot) -> None:
        """
        Removes a bot from the group

        Args:
            bot (Bot): The bot to remove
        """
        del self.bots[bot.nickname]

    def dumpj(self) -> Dict[str, Any]:
        """
        Returns the group in saveable format.

        Returns:
            Dict[str, Any]: The group in saveable dictionary format
        """
        raise NotImplementedError()

    def __iadd__(self, bot: Bot) -> "Group":
        """
        Adds a bot to the group.

        Args:
            bot (Bot): The bot to add.

        Raises:
            TypeError: In case your trying to add something but a bot.
            ValueError: If the bot (or a bot with the same nickname) 
                already exists in the group.
        """
        if not isinstance(bot, Bot):
            raise TypeError(f'Can\'t add {type(bot)} to group!')
        self.add(bot)
        return self

    def __isub__(self, bot: Bot) -> "Group":
        """
        Removes a bot from the group

        Args:
            bot (Bot): The bot to remove.

        Raises:
            TypeError: In case your trying to remove something but a bot.
        """
        if not isinstance(bot, Bot):
            raise TypeError(f'Can\'t remove {type(bot)} from group!')
        self.remove(bot)
        return self

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
