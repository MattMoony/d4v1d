
import lib.bot
from lib.bot.bot import Bot
from lib.platforms import Platform
from lib.db.dbc import DBController
from typing import *

class BotGroup(object):
    """A group of bots - useful for distributing tasks among many automated accounts"""

    def __init__(self, name: str, platform: Platform, db_controller: DBController):
        self.name: str = name
        self.platform: Platform = platform
        self.db_controller: DBController = db_controller
        self.bots: List[Bot] = []
        lib.bot.GROUPS.append(self)
    
    def __str__(self) -> str:
        return f'{self.name}({self.platform.name}, {len(self.bots)} bots, {round((len(self.get_authenticated())/max(len(self.bots), 1))*100)}% authenticated)'

    def get_authenticated(self) -> None:
        """Returns a list of all authenticated bots"""
        return list(filter(lambda b: b.username, self.bots))

    def add(self, username: Optional[str] = None, password: Optional[str] = None) -> None:
        """Adds a new bot to the group"""
        self.bots.append(Bot(self.platform, self.db_controller, username=username, password=password))

    def remove(self, idx: int) -> None:
        """Removes a bot from the group"""
        if 0 <= idx < len(self.bots):
            del self.bots[idx]
