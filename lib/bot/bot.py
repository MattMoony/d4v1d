from lib.errors import LoginFailedError
import requests as req
from lib.db import DBController
from lib.models.user import User
from lib.platforms import Platform
from typing import *

class Bot(object):
    """A bot - an automated user of a social-media platform."""

    def __init__(self, platform: Platform, db_controller: DBController, cookies: Optional[Dict[str, str]]=None, proxy: Optional[str] = None, 
                 headers: Optional[Dict[str, str]] = None, username: Optional[str] = None, password: Optional[str] = None):
        self.platform: Platform = platform
        self.db_controller: DBController = db_controller
        self.cookies: Optional[Dict[str, str]] = cookies
        self.proxy: Optional[str] = proxy
        self.headers: Dict[str, str] = { **self.platform.get_headers(), **headers, } if headers else self.platform.get_headers()
        self.session: req.Session = req.Session()
        if username:
            if not self.login(username, password):
                raise LoginFailedError()
        else:
            self.username: Optional[str] = None
        if self.cookies:
            self.__update_session_cookies()

    def __setattr__(self, name: str, value: Any) -> None:
        if name == 'proxy' and type(value) == str:
            self.session.proxies = { value.split(':')[0]: value, }
        elif name == 'headers':
            self.__dict__['headers'] = { **self.platform.get_headers(), **value, }
        elif name == 'cookies' and value:
            self.__dict__['cookies'] = { **(self.cookies if self.cookies else {}), **value, }
            self.__update_session_cookies()
        super().__setattr__(name, value)

    def __str__(self) -> str:
        return f'Bot({(self.username+"@") if self.username else ""}{self.platform.name})'
    
    def __update_session_cookies(self) -> None:
        """Apply the current cookies to the current session"""
        for c in self.cookies:
            self.session.cookies.set(**self.cookies[c])

    def login(self, username: str, password: str) -> bool:
        """Connects the bot with an account"""
        self.username = username
        return self.platform.login(self.session, username, password or '', headers=self.headers)

    def get_user(self, username: str) -> User:
        """Gets a basic overview of a social-media user"""
        u: User = self.platform.get_user(self.session, username, headers=self.headers)
        self.db_controller.store_user(u)
        return u
