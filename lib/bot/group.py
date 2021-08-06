
import lib.bot
from lib.bot.bot import Bot
from typing import *

class BotGroup(object):
    """A group of bots - useful for distributing tasks among many automated accounts"""

    def __init__(self, name: str):
        self.name: str = name
        self.bots: List[Bot] = []
        lib.bot.GROUPS.append(self)
    