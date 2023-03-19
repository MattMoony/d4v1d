"""
Contains the definition of the Group class,
i.e. a collection of Bot objects, which means
a collection of automated users / anonymous
browsers.
"""

from typing import Any, Dict, Optional

from d4v1d.platforms.instagram.bot.bot import InstagramBot
from d4v1d.platforms.instagram.db.models.user import InstagramUser
from d4v1d.platforms.platform.bot.group import Group
from d4v1d.platforms.platform.errors import EmptyGroupError
from d4v1d.platforms.platform.info import Info


class InstagramGroup(Group):
    """
    Group class - collection of Instagram bots.
    """

    def get_user(self, username: str) -> Optional[Info[InstagramUser]]:
        """
        Fetches info for the user with the given username

        Args:
            username (str): The username of the user

        Returns:
            Optional[Info[User]]: The user with the given username

        Raises:
            EmptyGroupException: If the group is empty
        """
        if not self.bots:
            raise EmptyGroupError()

        _minr: int = min(b.requests for b in self.bots)
        bot: InstagramBot = [ b for b in self.bots if b.requests == _minr ][0]
        return bot.get_user(username)

    def dumpj(self) -> Dict[str, Any]:
        """
        Returns the group in saveable format.

        Returns:
            Dict[str, Any]: The group in saveable dictionary format
        """
        return {
            'name': self.name,
            'bots': [ b.dumpj() for b in self.bots ],
        }

    @classmethod
    def loadj(cls, data: Dict[str, Any]) -> "InstagramGroup":
        """
        Loads the group from its saveable,
        dictionary format.

        Args:
            data (Dict[str, Any]): The saved format (dumpj)
        
        Returns:
            Platform: The re-constructed group
        """
        g: InstagramGroup = cls(
            name=data['name'],
        )
        g.bots = [ InstagramBot.loadj(b, g) for b in data['bots'] ]
        return g
