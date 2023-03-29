"""
Contains the definition of the Bot class,
i.e. an automated user / anonymous browser of 
Tellonym.
"""

import datetime
import json
import os
from typing import Any, Callable, Dict, List, Optional, Tuple

import requests as req

from d4v1d import config
from d4v1d.platforms.tellonym.db.models.tell import TellonymTell
from d4v1d.platforms.tellonym.db.models.user import TellonymUser
from d4v1d.platforms.platform.bot.bot import Bot
from d4v1d.platforms.platform.bot.group import Group
from d4v1d.platforms.platform.errors import (BadAPIResponseError)
from d4v1d.platforms.platform.info import Info


class TellonymBot(Bot):
    """
    Bot class - automated user of Tellonym.
    """

    username: str
    """The username of the bot"""
    password: str
    """The password of the bot"""
    session: req.Session
    """The session of the bot"""

    def __init__(self, nickname: str, group: "Group", anonymous: bool, user_agent: str, headers: Dict[str, str] = {}, creds: Optional[Tuple[str, str]] = None):
        """
        Creates a new TellonymBot object

        Args:
            nickname (str): The nickname of the bot (e.g. 'bot1')
            group (Group): The group the bot belongs to
            anonymous (bool): Whether the bot should be anonymous
            user_agent (str): The user agent of the bot
            headers (Dict[str, str]): The headers of the bot
            creds (Optional[Tuple[str, str]]): The credentials of the bot
        """
        super().__init__(nickname, group, anonymous)
        if not anonymous:
            if not isinstance(creds, tuple):
                raise TypeError('`creds` must be tuple of (<username>, <password>)!')
            if not creds:
                raise ValueError('`creds` must consist of <username> and <password>!')
            self.username, self.password = creds
        self.session = req.Session()
        self.session.headers.update({**headers, 'User-Agent': user_agent, })
        pass

    def debug(self) -> None:
        """
        Debugs the bot - drops into interactive IPython
        session with the bot.
        """
        bot: TellonymBot = self
        __import__('IPython').embed()
        pass

    def handle_error(self, r: req.Response) -> None:
        """
        Handles an error response from the Tellonym
        API - to raise a more fitting exception, should
        one exist.

        Args:
            r (req.Response): The error response to handle.
        """
        try:
            parsed: Dict[str, Any] = json.loads(r.text)
        except Exception:
            return
        pass

    def user(self, username: str) -> Optional[Info[TellonymUser]]:
        """
        Fetches info for the user with the given username

        Args:
            username (str): The username of the user

        Returns:
            Optional[Info[User]]: The user with the given username
        """
        r: req.Response = self.session.get(f'https://api.tellonym.me/profiles/name/{username}?limit=1')
        if not r.ok:
            return self.handle_error(r)
        _u: Dict[str, Any] = json.loads(r.text)
        ppath: str = ''
        stmp: datetime.datetime = datetime.datetime.now()
        if _u['avatarFileName']:
            r: req.Response = self.session.get(f'https://userimg.tellonym.me/lg-v2/{_u["avatarFileName"]}')
            if not r.ok:
                raise BadAPIResponseError(f'Could not fetch profile picture for user {username}')
            os.makedirs(os.path.join(config.PCONFIG._tellonym.ddir, 'users', username), exist_ok=True)
            ppath: str = os.path.join(config.PCONFIG._tellonym.ddir, 'users', username, f'{str(stmp.timestamp()).replace(".", "")}.jpg')
            with open(ppath, 'wb') as f:
                f.write(r.content)
        u: TellonymUser = TellonymUser.loadj(_u, api=True, profile_pic=ppath)
        return Info(u, stmp)

    def tells(self, user: TellonymUser, _from: Optional[datetime.datetime] = None, _to: Optional[datetime.datetime] = None) -> Optional[List[Info[TellonymTell]]]:
        fetch: Callable[[int, int], req.Response] = lambda _id, _after: self.session.get(f'https://api.tellonym.me/answers/{_id}?limit=100&pos={_after}')
        r: req.Response = fetch(user.id, 0)
        if not r.ok:
            return self.handle_error(r)
        tells: List[Info[TellonymTell]] = []
        now = datetime.datetime.now()
        while True:
            for _t in json.loads(r.text)['answers']:
                if ('tell' not in _t):
                    continue
                t: TellonymTell = TellonymTell.loadj(obj=_t, api=True)
                if (not _from or _from <= t.createdAt) and (not _to or t.createdAt <= _to):
                    t.owner = user
                    tells.append(Info(t, now))
            if len(json.loads(r.text)['answers']) <= 0:
                break
            r = fetch(user.id, len(tells) + 1)
            if not r.ok:
                return self.handle_error(r)
        return tells

    def dumpj(self) -> Dict[str, Any]:
        """
        Returns the bot in saveable format.

        Returns:
            Dict[str, Any]: The bot in saveable dictionary format
        """
        return {
            'nickname': self.nickname,
            'anonymous': self.anonymous,
            'user_agent': self.session.headers['User-Agent'],
            'headers': dict(self.session.headers),
            'creds': (self.username, self.password) if not self.anonymous else None,
        }

    def __str__(self) -> str:
        return f'"{self.nickname}"@Tellonym ({"anonymous" if self.anonymous else "authenticated"}))'

    def __repr__(self) -> str:
        return f'<{self}>'

    @classmethod
    def loadj(cls, data: Dict[str, Any], group: "Group") -> "TellonymBot":
        """
        Loads the bot from its saveable,
        dictionary format.

        Args:
            data (Dict[str, Any]): The saved format (dumpj)
            group: The group the bot belongs to
        
        Returns:
            Platform: The re-constructed bot
        """
        return TellonymBot(
            data['nickname'],
            group,
            not data['creds'],
            data['user_agent'],
            data['headers'],
            creds=data['creds'],
        )
