"""
Contains the Instagram class - the interface between
the core and this platform-specific implementation.
"""

import datetime
import json
import os
from typing import Any, Dict, List, Optional, Union

from d4v1d import config
from d4v1d.log import log
from d4v1d.platforms.instagram.bot.group import InstagramGroup
from d4v1d.platforms.instagram.cmd.add.bot import AddBot
from d4v1d.platforms.instagram.cmd.show.posts import ShowPosts
from d4v1d.platforms.instagram.db import DATABASES, Database
from d4v1d.platforms.instagram.db.models import InstagramUser
from d4v1d.platforms.instagram.db.models.post import InstagramPost
from d4v1d.platforms.platform import Platform
from d4v1d.platforms.platform.cmd.cmd import Command
from d4v1d.platforms.platform.errors import NoGroupsError, UnknownUserError
from d4v1d.platforms.platform.info import Info
from d4v1d.platforms.platform.ptaskopts import PTaskOpts
from d4v1d.platforms.platform.user import User


class Instagram(Platform):
    """
    Interface to https://www.instagram.com/
    """

    db: Database
    """The database for instagram info."""
    cmds: Dict[str, Union[Command, Dict[str, Any]]] = {
        'add': {
            'bot': AddBot(),
        },
        'show': {
            'posts': ShowPosts(),
        },
    }
    """The commands for this platform."""

    def __init__(self) -> None:
        """
        Creates a new Instagram object.
        """
        super().__init__("Instagram", "Wrapper for https://www.instagram.com/")
        log.debug('Initializing database of type "%s" ...', config.PCONFIG._instagram.db_type)
        self.db = DATABASES[config.PCONFIG._instagram.db_type]()

    def __del__(self) -> None:
        """
        Do some cleanup, once the platform is unloaded
        in the d4v1d core.
        """
        log.debug('Cleaning up Instagram ... ')
        with open(os.path.join(config.PCONFIG._instagram.cdir, 'instagram.json'), 'w', encoding='utf8') as f:
            log.debug('Backing up configured groups to "%s" ...', f.name)
            json.dump(self.dumpj(), f)
        del config.PCONFIG._instagram
        del self.db

    def group(self, name: str) -> InstagramGroup:
        """
        Create a new group with the given name.

        Returns:
            InstagramGroup: The new group.
        """
        log.debug('Creating new group "%s" ... ', name)
        return InstagramGroup(name)

    def user(self, username: str, opts: PTaskOpts = PTaskOpts()) -> Info[InstagramUser]:
        """
        Returns the user with the given username.

        Args:
            username (str): The username of the user.
            refresh (bool): Whether to force refresh the user info.
            group (Optional[InstagramGroup]): The group to use for fetching the user.

        Returns:
            Info[User]: The user info.
        """
        if not opts.refresh:
            log.debug('Check if user ("%s") is already part of the db', username)
            user: Optional[Info[InstagramUser]] = self.db.get_user(username)
            if user:
                log.debug('"%s" is already part of the db', username)
                return Info(user.value, user.date, self)
            log.debug('"%s" is not part of the db ... yet', username)
        log.debug('Fetching user info from instagram ... ')
        if not opts.group and not self.groups:
            raise NoGroupsError('No groups available for fetching user info.')
        user = (opts.group or list(self.groups.values())[0]).user(username)
        if not user:
            log.debug('"%s" is not known to instagram', username)
            raise UnknownUserError(f'"{username}" is not known to instagram')
        log.debug('Adding user to db ... ')
        self.db.store_user(user.value)
        return Info(user.value, user.date, self)

    def posts(self, username: str, download: bool = False, _from: Optional[datetime.datetime] = None,
              _to: Optional[datetime.datetime] = None, opts: PTaskOpts = PTaskOpts()) -> List[Info[InstagramPost]]:
        """
        Returns a list of all posts for the given usernames.

        Args:
            username (str): The username to fetch posts for.
            download (bool): Whether to download the posts (the media).
            _from (Optional[datetime.datetime]): The start date.
            _to (Optional[datetime.datetime]): The end date.
            opts (PTaskOpts): The options for the task.
        """
        user: InstagramUser = self.user(username, opts=PTaskOpts(group=opts.group)).value
        posts: List[Info[InstagramPost]] = []
        if not opts.refresh:
            log.debug('Check if posts of user ("%s") can be found in the db', username)
            posts: List[Info[InstagramPost]] = self.db.get_posts(user, _from=_from, _to=_to)
            log.debug('Found %d posts in db', len(posts))
            if len(posts) == user.number_posts:
                log.debug('Posts of user ("%s") can probably be found in the db', username)
            else:
                log.debug('Posts of user ("%s") can not be found in the db ... yet', username)
        if not posts:
            log.debug('Fetching posts from instagram ... ')
            if not opts.group and not self.groups:
                raise NoGroupsError('No groups available for fetching user\'s posts.')
            posts: List[Info[InstagramPost]] = (opts.group or list(self.groups.values())[0]).posts(user, _from=_from, _to=_to,)
            log.debug('Storing posts in db ... ')
            self.db.store_posts(posts)
        if download:
            (opts.group or list(self.groups.values())[0]).download_posts(posts)
            self.db.update_posts(posts)
        return posts

    def users(self) -> List[Info[InstagramUser]]:
        """
        Returns the list of locally cached users.

        Returns:
            List[str]: The list of local userrs.
        """
        return self.db.get_users()

    def dumpj(self) -> Dict[str, Any]:
        """
        To save-able format.
        """
        return {
            'groups': [ g.dumpj() for g in self.groups.values() ],
        }

    @classmethod
    def loadj(cls, data: Dict[str, Any]) -> "Platform":
        """
        Load saved data.
        """
        i: Instagram = Instagram()
        try:
            for v in data['groups']:
                g: InstagramGroup = InstagramGroup.loadj(v)
                i.groups[g.name] = g
        except Exception:  # pylint: disable=broad-exception-caught
            log.error('Instagram plaform file seems to be corrupted - continuing without saved groups, etc.')
        return i

    def __getitem__(self, username: str) -> User:
        """
        Get information about the user with the given 
        username; will **always** try to get the user 
        information from the local cache before scraping it.

        To get new, refreshed user information use
        the ``.user()`` method directly as it works
        for such requirements.

        Args:
            username (str): The user's username.

        Returns:
            User: The info about the user matching the username.

        Raises:
            KeyError: In case no user with the given
                username exists.
        """
        return self.user(username)
