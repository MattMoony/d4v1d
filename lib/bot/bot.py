import datetime
import requests as req
from lib import platforms, db
from lib.db import DBController
from lib.models import User, Media
from threading import Lock, Thread
from lib.platforms import Platform
from lib.errors import LoginFailedError
from typing import *

class Bot(object):
    """A bot - an automated user of a social-media platform."""

    """Is the bot currently doing work?"""
    occupied: bool = False
    """Lock for synchronizing occupied access across thread"""
    occupied_lock: Lock = Lock()
    """The task that the bot is currently working on"""
    task: Optional[Tuple[Tuple[Callable, List[Any], Dict[str, Any], Optional[Callable]]]] = None

    def __init__(self, platform: Platform, db_controller: DBController, cookies: Optional[Dict[str, str]]=None, proxy: Optional[str] = None, 
                 headers: Optional[Dict[str, str]] = None, username: Optional[str] = None, password: Optional[str] = None, group: Optional["BotGroup"] = None):
        self.platform: Platform = platform
        self.db_controller: DBController = db_controller
        self.headers: Dict[str, str] = { **self.platform.get_headers(), **headers, } if headers else self.platform.get_headers()
        self.group: Optional["BotGroup"] = group
        self.session: req.Session = req.Session()
        self.cookies: Dict[str, str] = cookies or {}
        self.proxy: Optional[str] = proxy
        if username and password:
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
        elif name == 'cookies' and value and 'cookies' in self.__dict__.keys():
            self.__dict__['cookies'] = { **(self.cookies or {}), **value, }
        super().__setattr__(name, value)
        if name == 'cookies' and value:
            self.__update_session_cookies()

    def __str__(self) -> str:
        return f'Bot({(self.username+"@") if self.username else ""}{self.platform.name})'

    @classmethod
    def unjson(cls, json: Dict[str, Any]) -> "Bot":
        """Creates a new bot with the given configuration"""
        return Bot(platforms.platform(json['platform']), db.CONTROLLERS[json['db_controller']], json['cookies'], json['proxy'], json['headers'], json['username'])

    def json(self) -> Dict[str, Any]:
        """Converts the bot's config to a dictionary"""
        return {
            'platform': self.platform.name,
            'db_controller': db.CONTROLLERS.index(self.db_controller),
            'cookies': self.cookies,
            'proxy': self.proxy,
            'headers': self.headers,
            'username': self.username,
        }
    
    def __update_session_cookies(self) -> None:
        """Apply the current cookies to the current session"""
        for k, v in self.cookies.items():
            self.session.cookies.set(k, v)

    def __poll_group(self) -> None:
        """Polls the group for something to do"""
        if not self.group:
            return
        with self.group.tasks_lock:
            if not self.group.tasks.empty():
                with self.occupied_lock:
                    if not self.occupied:
                        self.occupied = True
                        task: Tuple[Tuple[Callable, List[Any], Dict[str, Any], Optional[Callable]]] = self.group.tasks.pop(0)
        if task:
            Thread(target=self.do, args=task).start()

    def feierabend(self) -> None:
        """Finish work on the current task"""
        with self.occupied_lock:
            self.task = None
            self.occupied = False

    def do(self, task: Callable, args: List[Any], kwargs: Dict[str, Any], callback: Optional[Callable] = None) -> None:
        """Do an asynchronous task"""
        self.task = (task, args, kwargs, callback,)
        res: Any = getattr(self, task.__name__)(*args, **kwargs)
        self.feierabend()
        self.__poll_group()
        if callback:
            callback(res)

    def login(self, username: str, password: str) -> bool:
        """Connects the bot with an account"""
        self.username = username
        ret: bool = self.platform.login(self.session, username, password or '', headers=self.headers)
        self.cookies = self.session.cookies.get_dict()
        return ret

    def get_user(self, username: str) -> User:
        """Gets a basic overview of a social-media user"""
        u: User = self.platform.get_user(self.session, username, headers=self.headers)
        self.db_controller.store_user(u)
        return u

    def get_media(self, username: str, after: Optional[str] = None, timestamp: Optional[int] = None) -> Tuple[List[Media], str]:
        """Gets all media in a social-media account"""
        p: Tuple[int, str, str] = self.db_controller.get_platform(name=self.platform.name)
        u: User = self.db_controller.get_user(username, p[0])\
                  or self.get_user(username)
        if not timestamp:
            timestamp: int = self.db_controller.store_media_snapshot(username, p[0])
        media, after = self.platform.get_media(self.session, u.id, after=after, headers=self.headers)
        print(f'[*] Got {len(media)} media ... ')
        if self.group:
            if after:
                self.group.run(Bot.get_media, username, after=after, timestamp=timestamp)
            for m in media:
                self.group.run(Bot.download_media, u, m, timestamp=timestamp)
        return (media, after)

    def download_media(self, user: User, media: Media, timestamp: int = int(datetime.datetime.now().timestamp())) -> None:
        """Downloads the given media to disk"""
        print(f'[*] Downloading media "{media.name}" ... ')
        media.download(session=self.session, header=self.headers)
        p: Tuple[int, str, str] = self.db_controller.get_platform(name=self.platform.name)
        self.db_controller.store_media(user, p[0], timestamp, media)
