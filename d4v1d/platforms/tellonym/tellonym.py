"""
Contains the Tellonym class - the interface between
the core and this platform-specific implementation.
"""

import datetime
import json
import os
from typing import Any, Dict, List, Optional, Union

from d4v1d import config
from d4v1d.log import log
from d4v1d.platforms.tellonym.bot.group import TellonymGroup
from d4v1d.platforms.tellonym.cmd.add.bot import AddBot
from d4v1d.platforms.tellonym.cmd.show.tells import ShowTells
from d4v1d.platforms.tellonym.db import DATABASES, Database
from d4v1d.platforms.tellonym.db.models.user import TellonymUser
from d4v1d.platforms.tellonym.db.models.tell import TellonymTell
from d4v1d.platforms.platform import Platform
from d4v1d.platforms.platform.cmd.cmd import Command
from d4v1d.platforms.platform.errors import NoGroupsError, UnknownUserError
from d4v1d.platforms.platform.info import Info

class Tellonym(Platform):
    """
    Interface to https://www.tellonym.me/
    """

    db: Database
    """The database for tellonym info."""
    cmds: Dict[str, Union[Command, Dict[str, Any]]] = {
        'add': {
            'bot': AddBot(),
        },
        'show': {
            'tells': ShowTells(),
        },
    }
    """The commands for this platform."""

    def __init__(self) -> None:
        """
        Creates a new Tellonym object.
        """
        super().__init__("Tellonym", "Wrapper for https://www.tellonym.me/")
        log.debug('Initializing database of type "%s" ...', config.PCONFIG._tellonym.db_type)
        self.db = DATABASES[config.PCONFIG._tellonym.db_type]()

    def __del__(self) -> None:
        """
        Do some cleanup, once the platform is unloaded
        in the d4v1d core.
        """
        log.debug('Cleaning up Tellonym ... ')
        with open(os.path.join(config.PCONFIG._tellonym.cdir, 'tellonym.json'), 'w', encoding='utf8') as f:
            log.debug('Backing up configured groups to "%s" ...', f.name)
            json.dump(self.dumpj(), f)
        del config.PCONFIG._tellonym
        del self.db

    def group(self, name: str) -> TellonymGroup:
        """
        Create a new group with the given name.

        Returns:
            TellonymGroup: The new group.
        """
        log.debug('Creating new group "%s" ... ', name)
        return TellonymGroup(name)

    def user(self, username: str, refresh: bool = False, group: Optional[TellonymGroup] = None) -> Info[TellonymUser]:
        """
        Returns the user with the given username.

        Args:
            username (str): The username of the user.
            refresh (bool): Whether to force refresh the user info.
            group (Optional[TellonymGroup]): The group to use for fetching the user.

        Returns:
            Info[User]: The user info.
        """
        if not refresh:
            log.debug('Check if user ("%s") is already part of the db', username)
            user: Optional[Info[TellonymUser]] = self.db.get_user(username)
            if user:
                log.debug('"%s" is already part of the db', username)
                return Info(user.value, user.date, self)
            log.debug('"%s" is not part of the db ... yet', username)
        log.debug('Fetching user info from tellonym ... ')
        if not group and not self.groups:
            raise NoGroupsError('No groups available for fetching user info.')
        user = (group or list(self.groups.values())[0]).user(username)
        if not user:
            log.debug('"%s" is not known to tellonym', username)
            raise UnknownUserError(f'"{username}" is not known to tellonym')
        log.debug('Adding user to db ... ')
        self.db.store_user(user.value)
        return Info(user.value, user.date, self)

    def tells(self, username: str, _from: Optional[datetime.datetime] = None,
              _to: Optional[datetime.datetime] = None, refresh: bool = False, group: Optional[TellonymGroup] = None) -> List[Info[TellonymTell]]:
        """
        Returns a list of all tells for the given usernames.

        Args:
            username (str): The username to fetch tells for.
            _from (Optional[datetime.datetime]): The start date.
            _to (Optional[datetime.datetime]): The end date.
            refresh (bool): Whether to force refresh the tells.
            group (Optional[TellonymGroup]): The group to use for fetching the tells.
        """
        user: TellonymUser = self.user(username, group=group).value
        if not refresh:
            log.debug('Check if tells of user ("%s") can be found in the db', username)
            tells: List[Info[TellonymTell]] = self.db.get_tells(user, _from=_from, _to=_to)
            log.debug('Found %d tells in db', len(tells))
            if len(tells) == user.number_posts:
                log.debug('tells of user ("%s") can probably be found in the db', username)
            else:
                log.debug('tells of user ("%s") can not be found in the db ... yet', username)
        if not tells:
            log.debug('Fetching tells from tellonym ... ')
            if not group and not self.groups:
                raise NoGroupsError('No groups available for fetching user\'s tells.')
            tells: List[Info[TellonymTell]] = (group or list(self.groups.values())[0]).tells(user, _from=_from, _to=_to,)
            log.debug('Storing tells in db ... ')
            self.db.store_tells(tells)
        return tells

    def users(self) -> List[Info[TellonymUser]]:
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
        i: Tellonym = Tellonym()
        try:
            for v in data['groups']:
                g: TellonymGroup = TellonymGroup.loadj(v)
                i.groups[g.name] = g
        except Exception:  # pylint: disable=broad-exception-caught
            log.error('Tellonym plaform file seems to be corrupted - continuing without saved groups, etc.')
        return i