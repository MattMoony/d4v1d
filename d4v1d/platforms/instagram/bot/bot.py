"""
Contains the definition of the Bot class,
i.e. an automated user / anonymous browser of 
Instagram.
"""

import os
import json
import datetime
import requests as req
import d4v1d.config as config
from d4v1d.platforms.platform.bot.bot import Bot
from d4v1d.platforms.platform.bot.group import Group
from d4v1d.platforms.instagram.db.models.user import User
from typing import *
from d4v1d.platforms.platform.errors import BadAPIResponseError

from d4v1d.platforms.platform.info import Info

class InstagramBot(Bot):
    """
    Bot class - automated user of Instagram.
    """

    username: str
    """The username of the bot"""
    password: str
    """The password of the bot"""
    session: req.Session
    """The session of the bot"""
    
    def __init__(self, group: Group, anonymous: bool, user_agent: str, headers: Dict[str, str] = {},
                 creds: Optional[Tuple[str, str]] = None):
        """
        Creates a new InstagramBot object

        Args:
            group (Group): The group the bot belongs to
            anonymous (bool): Whether the bot should be anonymous
            user_agent (str): The user agent of the bot
            headers (Dict[str, str]): The headers of the bot
            creds (Optional[Tuple[str, str]]): The credentials of the bot
        """
        super().__init__(group, anonymous)
        if not anonymous:
            self.username, self.password = creds

        self.session = req.Session()
        self.session.headers.update({ **headers, 'User-Agent': user_agent, })

    def get_user(self, username: str) -> Optional[Info[User]]:
        """
        Fetches info for the user with the given username

        Args:
            username (str): The username of the user

        Returns:
            Optional[Info[User]]: The user with the given username
        """
        r: req.Response = self.session.get(f'https://www.instagram.com/{username}/?__a=1&__d=1')
        if not r.ok:
            return None
        _u: Dict[str, Any] = json.loads(r.text)['graphql']['user']
        r = self.session.get(_u['profile_pic_url_hd'])
        if not r.ok:
            raise BadAPIResponseError(f'Could not fetch profile picture for user {username}')
        stmp: datetime.datetime = datetime.datetime.now()
        os.makedirs(os.path.join(config.PCONFIG._instagram.ddir, 'users', username), exist_ok=True)
        ppath: str = os.path.join(config.PCONFIG._instagram.ddir, 'users', username, f'{stmp.timestamp().replace(".", "_")}.jpg')
        with open(ppath, 'wb') as f:
            f.write(r.content)
        u: User = User.loadj(_u, api=True, profile_pic=ppath)
        return Info(u, stmp)
