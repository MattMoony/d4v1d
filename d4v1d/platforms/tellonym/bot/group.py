"""
Contains the definition of the Group class,
i.e. a collection of Bot objects, which means
a collection of automated users / anonymous
browsers.
"""

import datetime
from multiprocessing import Lock
from typing import Any, Dict, List, Optional

from d4v1d.platforms.tellonym.bot.bot import TellonymBot
from d4v1d.platforms.tellonym.db.models.tell import TellonymTell
from d4v1d.platforms.tellonym.db.models.user import TellonymUser
from d4v1d.platforms.platform.bot.group import Group
from d4v1d.platforms.platform.errors import EmptyGroupError
from d4v1d.platforms.platform.info import Info


class TellonymGroup(Group):
    """
    Group class - collection of Tellonym bots.
    """

    def bot(self, _safety_lock: Optional[Lock] = None) -> TellonymBot:
        """
        Returns a bot from the group; preferably the
        one that's made the least requests so far.

        Returns:
            InstagramBot: A bot from the group.
        """
        if not self.bots:
            raise EmptyGroupError()
        _minr: int = min(b.requests for b in self.bots.values())
        minb: TellonymBot = [ b for b in self.bots.values() if b.requests == _minr ][0]
        if _safety_lock is not None:
            _safety_lock.release()
        return minb

    def user(self, username: str) -> Optional[Info[TellonymUser]]:
        """
        Fetches info for the user with the given username

        Args:
            username (str): The username of the user

        Returns:
            Optional[Info[User]]: The user with the given username

        Raises:
            EmptyGroupException: If the group is empty
        """
        return self.bot().user(username)
    
    def tells(self, user: TellonymUser, _from: Optional[datetime.datetime] = None, _to: Optional[datetime.datetime] = None) -> List[Info[TellonymTell]]:
        try:
            return self.bot().tells(user, _from, _to)
        except Exception as e:
            import traceback
            traceback.print_exception(e)
    pass

    def dumpj(self) -> Dict[str, Any]:
        """
        Returns the group in saveable format.

        Returns:
            Dict[str, Any]: The group in saveable dictionary format
        """
        return {
            'name': self.name,
            'bots': [ b.dumpj() for b in self.bots.values() ],
        }

    @classmethod
    def loadj(cls, data: Dict[str, Any]) -> "TellonymGroup":
        """
        Loads the group from its saveable,
        dictionary format.

        Args:
            data (Dict[str, Any]): The saved format (dumpj)
        
        Returns:
            Platform: The re-constructed group
        """
        g: TellonymGroup = cls(
            name=data['name'],
        )
        _bots: List[TellonymBot] = [ TellonymBot.loadj(b, g) for b in data['bots'] ]
        g.bots = { b.nickname: b for b in _bots }
        return g

    