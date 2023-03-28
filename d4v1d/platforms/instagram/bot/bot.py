"""
Contains the definition of the Bot class,
i.e. an automated user / anonymous browser of 
Instagram.
"""

import datetime
import json
import os
from typing import Any, Callable, Dict, List, Optional, Tuple

import requests as req

from d4v1d import config
from d4v1d.log import log
from d4v1d.platforms.instagram.db.models.post import InstagramPost
from d4v1d.platforms.instagram.db.models.user import InstagramUser
from d4v1d.platforms.platform.bot.bot import Bot
from d4v1d.platforms.platform.bot.group import Group
from d4v1d.platforms.platform.errors import (BadAPIResponseError,
                                             RateLimitError,
                                             RequiresAuthenticationError)
from d4v1d.platforms.platform.info import Info
from d4v1d.platforms.platform.mediatype import MediaType
from d4v1d.utils.anonsession import AnonSession


class InstagramBot(Bot):
    """
    Bot class - automated user of Instagram.
    """

    username: str
    """The username of the bot"""
    password: str
    """The password of the bot"""
    session: AnonSession
    """The session of the bot"""

    def __init__(self, nickname: str, group: Group, anonymous: bool, user_agent: str, headers: Dict[str, str] = {},  # pylint: disable=dangerous-default-value
                 creds: Optional[Tuple[str, str]] = None):
        """
        Creates a new InstagramBot object

        Args:
            nickname (str): The nickname of the bot (e.g. 'bot1')
            group (Group): The group the bot belongs to
            anonymous (bool): Whether the bot should be anonymous
            user_agent (str): The user agent of the bot (deprecated).
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

        self.session = AnonSession(shapeshift=anonymous)
        self.session.headers.update({ **headers })

    def debug(self) -> None:
        """
        Debugs the bot - drops into interactive IPython
        session with the bot.
        """
        bot: InstagramBot = self
        __import__('IPython').embed()

    def handle_error(self, r: req.Response) -> None:
        """
        Handles an error response from the Instagram
        API - to raise a more fitting exception, should
        one exist.

        Args:
            r (req.Response): The error response to handle.
        """
        try:
            parsed: Dict[str, Any] = json.loads(r.text)
        except Exception:
            return
        if 'message' in parsed and 'wait' in parsed['message']:
            raise RateLimitError(parsed['message'])
        if 'require_login' in parsed and parsed['require_login']:
            raise RequiresAuthenticationError('Instagram is asking the bot to authenticate.')

    def user(self, username: str) -> Optional[Info[InstagramUser]]:
        """
        Fetches info for the user with the given username

        Args:
            username (str): The username of the user

        Returns:
            Optional[Info[User]]: The user with the given username
        """
        r: req.Response = self.session.get(f'https://www.instagram.com/{username}/?__a=1&__d=1')
        if not r.ok:
            return self.handle_error(r)
        _u: Dict[str, Any] = json.loads(r.text)['graphql']['user']
        r = self.session.get(_u['profile_pic_url_hd'])
        if not r.ok:
            raise BadAPIResponseError(f'Could not fetch profile picture for user {username}')
        stmp: datetime.datetime = datetime.datetime.now()
        os.makedirs(os.path.join(config.PCONFIG._instagram.ddir, 'users', username), exist_ok=True)  # pylint: disable=protected-access
        ppath: str = os.path.join(config.PCONFIG._instagram.ddir, 'users', username, f'{str(stmp.timestamp()).replace(".", "_")}.jpg')  # pylint: disable=protected-access
        with open(ppath, 'wb') as f:
            f.write(r.content)
        u: InstagramUser = InstagramUser.loadj(_u, api=True, profile_pic=ppath)
        return Info(u, stmp)
    
    def posts(self, user: InstagramUser, _from: Optional[datetime.datetime] = None, 
              _to: Optional[datetime.datetime] = None) -> Optional[List[Info[InstagramPost]]]:
        """
        Returns a list of all posts this user has made; while caching
        them locally - meaning also downloading & storing the actual images.

        Args:
            user (InstagramUser): The instagram user, whose posts to get.
            _from (Optional[datetime.datetime]): The earliest date to fetch posts from.
            _to (Optional[datetime.datetime]): The latest date to fetch posts from.

        Returns:
            List[Info[InstagramPost]]: The list of posts.
        """
        fetch: Callable[[int, Optional[str]], req.Response] = lambda _id, _after: self.session.get(f'https://www.instagram.com/graphql/query/', params={
            'query_hash': 'e769aa130647d2354c40ea6a439bfc08',
            'variables': json.dumps({"id": _id, "first": 10, "after": _after,}),
        })
        r: req.Response = fetch(user.id, None)
        if not r.ok:
            return self.handle_error(r)
        posts: List[Info[InstagramPost]] = []
        while True:
            _b: Dict[str, Any] = json.loads(r.text)['data']['user']['edge_owner_to_timeline_media']
            for _p in _b['edges']:
                p: InstagramPost = InstagramPost.loadj(_p['node'], api=True)
                p.owner = user
                if (not _from or _from <= p.taken_at) and (not _to or p.taken_at <= _to):
                    posts.append(Info(p, datetime.datetime.now()))
            if not _b['page_info']['has_next_page']:
                break
            r = fetch(user.id, _b["page_info"]["end_cursor"])
            if not r.ok:
                return self.handle_error(r)
        return posts

    def download_post(self, post: Info[InstagramPost]) -> None:
        """
        Downloads the post and stores it locally.

        Args:
            post (Info[InstagramPost]): The post to download.
        """
        log.info('Downloading post %s', post.value.short_code)
        p: InstagramPost = post.value
        os.makedirs(os.path.join(config.PCONFIG._instagram.ddir, 'users', p.owner.username, p.short_code), exist_ok=True)
        for i, m in enumerate(p.media):
            log.debug('Downloading media %s with %s', m.url, str(self))
            m.path = os.path.join(config.PCONFIG._instagram.ddir, 'users', p.owner.username, p.short_code, f'{str(post.date.timestamp()).replace(".", "_")}_{i}.{"jpg" if m.type == MediaType.IMAGE else "mp4"}')
            # don't overwrite already downloaded files, as this is
            # probably unwanted behaviour, but could happen, if the user
            # tells d4v1d to download locally cached posts - yk
            if os.path.exists(m.path):
                continue
            r: req.Response = self.session.get(m.url)
            if not r.ok:
                raise BadAPIResponseError(f'Could not fetch post {p.id} from {m.url}')
            with open(m.path, 'wb') as f:
                f.write(r.content)

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
        return f'"{self.nickname}"@Instagram ({"anonymous" if self.anonymous else "authenticated"}))'

    def __repr__(self) -> str:
        return f'<{self}>'

    @classmethod
    def loadj(cls, data: Dict[str, Any], group: "Group") -> "InstagramBot":
        """
        Loads the bot from its saveable,
        dictionary format.

        Args:
            data (Dict[str, Any]): The saved format (dumpj)
            group: The group the bot belongs to
        
        Returns:
            Platform: The re-constructed bot
        """
        return InstagramBot(
            data['nickname'],
            group,
            not data['creds'],
            data['user_agent'],
            data['headers'],
            creds=data['creds'],
        )
