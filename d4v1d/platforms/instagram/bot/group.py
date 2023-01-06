"""
Contains the definition of the Group class,
i.e. a collection of Bot objects, which means
a collection of automated users / anonymous
browsers.
"""

from d4v1d.platforms.platform.info import Info
from d4v1d.platforms.platform.bot.group import Group
from d4v1d.platforms.instagram.db.models.user import User
from d4v1d.platforms.instagram.bot.bot import InstagramBot
from d4v1d.platforms.platform.errors import EmptyGroupError
from typing import *

class InstagramGroup(Group):
    """
    Group class - collection of Instagram bots.
    """

    def get_user(self, username: str) -> Optional[Info[User]]:
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
