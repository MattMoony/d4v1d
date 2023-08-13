"""
Contains the definition of the Group class,
i.e. a collection of Bot objects, which means
a collection of automated users / anonymous
browsers.
"""

import datetime
from multiprocessing import Lock, Manager, Pool
from multiprocessing.managers import DictProxy
from typing import Any, Dict, List, Optional

from d4v1d import config
from d4v1d.log import log
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
        _minr: int = min(b.requests for b in self.bots.values())
        minb: InstagramBot = [ b for b in self.bots.values() if b.requests == _minr ][0]
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
        bot: InstagramBot = self.bot()
        return bot.posts(user, _from, _to)

    def download_posts(self, posts: List[Info[InstagramPost]]) -> None:
        """
        Downloads all the posts in the given list.

        Args:
            posts (List[Info[InstagramPost]]): The list of posts to download.
        """
        log.info('Downloading %d posts using a max of %d bots in parallel ...', len(posts), config.PCONFIG._instagram.max_parallel_downloads)  # pylint: disable=protected-access
        with Manager() as manager:
            bots_lock: Lock = manager.Lock()
            constraints: DictProxy = manager.dict({
                _: manager.Semaphore(config.PCONFIG._instagram.max_parallel_downloads_per_bot)  # pylint: disable=no-member, protected-access
                for _ in self.bots
            })
            # in order to allow local media paths to be updated
            # after the media has been stored there - all while
            # using a threaded approach -> use this helper proxy
            media_paths: DictProxy = manager.dict({
                p.value.short_code: manager.dict({
                    m.id: None
                    for m in p.value.media
                })
                for p in posts
            })
            with Pool(processes=config.PCONFIG._instagram.max_parallel_downloads) as pool:  # pylint: disable=protected-access
                pool.starmap(self._download_post, [ (p, constraints, bots_lock, media_paths[p.value.short_code], config.PCONFIG._instagram.ddir,) 
                                                    for p in posts ])
            log.info('Done downloading %d posts.', len(posts))
            # actually update the local media paths for the posts;
            # since pass by reference wasn't possible due to multiprocessing ...
            for m in [ m for p in posts for m in p.value.media ]:
                m.path = media_paths[m.post.short_code][m.id]

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

    def _download_post(self, post: Info[InstagramPost], constraints: DictProxy, bots_lock: Lock, media_paths: DictProxy,
                       ddir: str) -> None:
        """
        Downloads the given post (threaded).

        Args:
            post (Info[InstagramPost]): The post to download.
            constraints (DictProxy): The constraints for each bot.
            bots_lock (Lock): The lock to use for thread safety.
            media_paths (DictProxy): The media paths for the post (for parallelism; yk, cause only pass by value, etc.).
            ddir (str): The data / output directory for the media (for parallelism as well, yk)
        """
        bot: InstagramBot = self.bot(_safety_lock=bots_lock)
        with constraints[bot.nickname]:
            bot.download_post(post, media_paths=media_paths, ddir=ddir)

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
        _bots: List[InstagramBot] = [ InstagramBot.loadj(b, g) for b in data['bots'] ]
        g.bots = { b.nickname: b for b in _bots }
        return g
