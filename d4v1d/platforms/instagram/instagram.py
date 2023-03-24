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

    def user(self, username: str, refresh: bool = False, group: Optional[InstagramGroup] = None) -> Info[InstagramUser]:
        """
        Returns the user with the given username.

        Args:
            username (str): The username of the user.
            refresh (bool): Whether to force refresh the user info.
            group (Optional[InstagramGroup]): The group to use for fetching the user.

        Returns:
            Info[User]: The user info.
        """
        if not refresh:
            log.debug('Check if user ("%s") is already part of the db', username)
            user: Optional[Info[InstagramUser]] = self.db.get_user(username)
            if user:
                log.debug('"%s" is already part of the db', username)
                return Info(user.value, user.date, self)
            log.debug('"%s" is not part of the db ... yet', username)
        log.debug('Fetching user info from instagram ... ')
        if not group and not self.groups:
            raise NoGroupsError('No groups available for fetching user info.')
        user = (group or list(self.groups.values())[0]).user(username)
        if not user:
            log.debug('"%s" is not known to instagram', username)
            raise UnknownUserError(f'"{username}" is not known to instagram')
        log.debug('Adding user to db ... ')
        self.db.store_user(user.value)
        return Info(user.value, user.date, self)
    
    def posts(self, username: str, download: bool = False, _from: Optional[datetime.datetime] = None,
              _to: Optional[datetime.datetime] = None, refresh: bool = False, group: Optional[InstagramGroup] = None) -> List[Info[InstagramPost]]:
        """
        Returns a list of all posts for the given usernames.

        Args:
            username (str): The username to fetch posts for.
            download (bool): Whether to download the posts (the media).
            _from (Optional[datetime.datetime]): The start date.
            _to (Optional[datetime.datetime]): The end date.
            refresh (bool): Whether to force refresh the posts.
            group (Optional[InstagramGroup]): The group to use for fetching the posts.
        """
        # TODO: finish implementation
        if not group and not self.groups:
            raise NoGroupsError('No groups available for fetching user\'s posts.')
        user: InstagramUser = self.user(username, group=group).value
        posts: List[Info[InstagramPost]] = (group or list(self.groups.values())[0]).posts(user, _from=_from, _to=_to,)
        if download:
            (group or list(self.groups.values())[0]).download_posts(posts)
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
