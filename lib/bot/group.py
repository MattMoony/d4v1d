
import lib.bot
from queue import Queue
from lib.bot.bot import Bot
from lib.platforms import Platform
from threading import Thread, Lock
from lib.db.dbc import DBController
from typing import *

class BotGroup(object):
    """A group of bots - useful for distributing tasks among many automated accounts"""

    """The tasks that should be distributed"""
    tasks: List[Tuple[Tuple[Callable, List[Any], Dict[str, Any], Optional[Callable]]]] = []
    """Lock for synchronizing task access across threads"""
    tasks_lock: Lock = Lock()

    """The list of bots in the bot-group"""
    bots: List[Bot] = []
    """Lock for synchronizing bots access across threads"""
    bots_lock: Lock = Lock()

    def __init__(self, name: str, platform: Platform, db_controller: DBController):
        self.name: str = name
        self.platform: Platform = platform
        self.db_controller: DBController = db_controller
        lib.bot.GROUPS.append(self)
    
    def __str__(self) -> str:
        return f'{self.name}({self.platform.name}, {len(self.bots)} bots, {round((len(self.get_authenticated())/max(len(self.bots), 1))*100)}% authenticated)'

    def get_authenticated(self) -> None:
        """Returns a list of all authenticated bots"""
        with self.bots_lock:
            return list(filter(lambda b: b.username, self.bots))

    def add(self, username: Optional[str] = None, password: Optional[str] = None) -> None:
        """Adds a new bot to the group"""
        with self.bots_lock:
            self.bots.append(Bot(self.platform, self.db_controller, username=username, password=password))

    def remove(self, idx: int) -> None:
        """Removes a bot from the group"""
        with self.bots_lock:
            if 0 <= idx < len(self.bots):
                del self.bots[idx]

    def run(self, task: Callable, *args: List[Any], callback: Optional[Callable] = None, **kwargs: Dict[str, Any]) -> None:
        """Adds & runs a task"""
        with self.bots_lock:
            for b in self.bots:
                with b.occupied_lock:
                    if not b.occupied:
                        b.occupied = True
                        Thread(target=b.do, args=(task, args, kwargs, callback,)).start()
                        return
        with self.tasks_lock:
            self.tasks.append((task, args, kwargs, callback,))
