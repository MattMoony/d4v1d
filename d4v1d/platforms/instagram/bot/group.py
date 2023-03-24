"""
Contains the definition of the Group class,
i.e. a collection of Bot objects, which means
a collection of automated users / anonymous
browsers.
"""

import datetime
from multiprocessing import Lock, Manager, Pool
from multiprocessing.managers import ListProxy
from typing import Any, Dict, List, Optional

from d4v1d import config
from d4v1d.platforms.instagram.bot.bot import InstagramBot
from d4v1d.platforms.instagram.db.models.post import InstagramPost
from d4v1d.platforms.instagram.db.models.user import InstagramUser
from d4v1d.platforms.platform.bot.group import Group
from d4v1d.platforms.platform.errors import EmptyGroupError
from d4v1d.platforms.platform.info import Info


class InstagramGroup(Group):
    """
    Group class - collection of Instagram bots.
    """

    def bot(self, _safety_lock: Optional[Lock] = None) -> InstagramBot:
        """
        Returns a bot from the group; preferably the
        one that's made the least requests so far.

        Returns:
            InstagramBot: A bot from the group.
        """
        if not self.bots:
            raise EmptyGroupError()
        
        if _safety_lock is not None:
            _safety_lock.acquire()
        _minr: int = min(b.requests for b in self.bots)
        minb: InstagramBot = [ b for b in self.bots if b.requests == _minr ][0]
        if _safety_lock is not None:
            _safety_lock.release()
        return minb

    def user(self, username: str) -> Optional[Info[InstagramUser]]:
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
    
    def posts(self, user: InstagramUser, _from: Optional[datetime.datetime] = None,
              _to: Optional[datetime.datetime] = None) -> List[Info[InstagramPost]]:
        """
        Returns a list of all posts this user has made.

        Args:
            username (InstagramUser): The user.
            _from (Optional[datetime.datetime]): The earliest date to fetch posts from.
            _to (Optional[datetime.datetime]): The latest date to fetch posts from.

        Returns:
            List[Info[InstagramPost]]: The list of posts.
        """
        try:
            bot: InstagramBot = self.bot()
            return bot.posts(user, _from, _to)
        except Exception as e:
            import traceback
            traceback.print_exception(e)
    
    def download_posts(self, posts: List[Info[InstagramPost]]) -> None:
        """
        Downloads all the posts in the given list.

        Args:
            posts (List[Info[InstagramPost]]): The list of posts to download.
        """
        with Manager() as manager:
            bots_lock: Lock = manager.Lock()
            constraints: ListProxy = manager.list([
                manager.Semaphore(config.PCONFIG._instagram.max_parallel_downloads_per_bot) for _ in self.bots 
            ])
            with Pool(processes=config.PCONFIG._instagram.max_parallel_downloads) as pool:
                pool.starmap(self._download_post, [ (p, constraints, bots_lock,) for p in posts ])

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
    
    def _download_post(self, post: Info[InstagramPost], constraints: ListProxy, bots_lock: Lock) -> None:
        """
        Downloads the given post (threaded).

        Args:
            post (Info[InstagramPost]): The post to download.
            constraints (ListProxy): The constraints for each bot.
            bots_lock (Lock): The lock to use for thread safety.
        """
        bot: InstagramBot = self.bot(_safety_lock=bots_lock)
        bots_lock.acquire()
        boti: int = self.bots.index(bot)
        bots_lock.release()
        # TODO: could probably improve this whole constraints
        # situation, as it looks a little messy right now; but
        # yes... perhaps need to introduce some sort of unique
        # bot id (perhaps nickname) for this? :thinking:
        with constraints[boti]:
            bot.download_post(post)

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
