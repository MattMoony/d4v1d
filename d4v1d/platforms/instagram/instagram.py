"""
Contains the Instagram class - the interface between
the core and this platform-specific implementation.
"""

import json
import os
from typing import Any, Dict, List, Optional, Union

from d4v1d import config
from d4v1d.log import log
from d4v1d.platforms.instagram.bot.group import InstagramGroup
from d4v1d.platforms.instagram.cmd.add.bot import AddBot
from d4v1d.platforms.instagram.db import DATABASES, Database
from d4v1d.platforms.instagram.db.models import User
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
    }
    """The commands for this platform."""

    def __init__(self):
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

    def add_group(self, name: str) -> None:
        """
        Adds a new group with the given name.

        Args:
            name (str): The name of the group.
        """
        log.debug('Adding group "%s" ... ', name)
        self.groups[name] = InstagramGroup(name)

    def rm_group(self, name: str) -> None:
        """
        Removes the group with the given name.

        Args:
            name (str): The name of the group.
        """
        log.debug('Removing group "%s" ... ', name)
        del self.groups[name]

    def get_user(self, username: str, refresh: bool = False, group: Optional[InstagramGroup] = None) -> Info[User]:
        """
        Returns the user with the given username

        Args:
            username (str): The username of the user.
            refresh (bool): Whether to force refresh the user info.
            group (Optional[InstagramGroup]): The group to use for fetching the user.

        Returns:
            Info[User]: The user info.
        """
        if not refresh:
            log.debug('Check if user ("%s") is already part of the db', username)
            user: Optional[Info[User]] = self.db.get_user(username)
            if user:
                log.debug('"%s" is already part of the db', username)
                return Info(user.value, user.date, self)
            log.debug('"%s" is not part of the db ... yet', username)
        log.debug('Fetching user info from instagram ... ')
        if not group and not self.groups:
            raise NoGroupsError('No groups available for fetching user info')
        user = (group or list(self.groups.values())[0]).get_user(username)
        if not user:
            log.debug('"%s" is not known to instagram', username)
            raise UnknownUserError(f'"{username}" is not known to instagram')
        log.debug('Adding user to db ... ')
        self.db.store_user(user.value)
        return Info(user.value, user.date, self)
    
    def get_cached_usernames(self) -> List[str]:
        """
        Returns the list of usernames whose info has been cached
        locally.

        Returns:
            List[str]: The list of usernames.
        """
        return [ u.value.username for u in self.db.get_users() ]

    def get_user_description(self, username: str, refresh: bool = False, group: Optional[InstagramGroup] = None) -> Info[str]:
        """
        Returns the description of the user with the given username.

        Args:
            username (str): The username of the user.
            refresh (bool): Whether to force refresh the user info.
            group (Optional[InstagramGroup]): The group to use for fetching the user.

        Returns:
            Info[str]: The description of the user.
        """
        i: Info[User] = self.get_user(username, refresh=refresh, group=group)
        if i:
            return Info(i.value.bio, i.date, self)
        return None

    def get_user_profile_pic(self, username: str, refresh: bool = False, group: Optional[InstagramGroup] = None) -> Info[str]:
        """
        Returns the profile picture of the user with the given username.

        Args:
            username (str): The username of the user.
            refresh (bool): Whether to force refresh the user info.
            group (Optional[InstagramGroup]): The group to use for fetching the user.

        Returns:
            Info[str]: The profile picture of the user.
        """
        i: Info[User] = self.get_user(username, refresh=refresh, group=group)
        if i:
            return Info(i.value.profile_pic, i.date, self)
        return None

    def get_user_number_posts(self, username: str, refresh: bool = False, group: Optional[InstagramGroup] = None) -> Info[int]:
        """
        Returns the number of posts of the user with the given username.

        Args:
            username (str): The username of the user.
            refresh (bool): Whether to force refresh the user info.
            group (Optional[InstagramGroup]): The group to use for fetching the user.

        Returns:
            Info[int]: The number of posts of the user.
        """
        i: Info[User] = self.get_user(username, refresh=refresh, group=group)
        if i:
            return Info(i.value.number_posts, i.date, self)
        return None

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
