"""
Contains the definition of the Group class,
i.e. a collection of Bot objects, which means
a collection of automated users / anonymous
browsers.
"""

from .bot import Bot
from typing import *

class Group(object):
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
