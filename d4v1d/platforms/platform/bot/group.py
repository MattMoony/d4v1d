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

    def __init__(self, name: str, bots: List[Bot] = []):
        """
        Initialize the group with a name and an 
        optional list of bots.

        Args:
            name (str): The name of the group
            bots (List[Bot], optional): The bots in the group. Defaults to [].
        """
        self.name = name
        self.bots = bots
