"""
All wrappers for the private API are implemented here. (private endpoints --> need to be authenticated, maybe authorized)
"""

from lib import models, local, db
from lib.api import urls, params, base, public
import time, random, uuid, hmac, json, hashlib, os, threading, datetime
import requests as req
import six.moves.urllib as urllib
from typing import List, Dict, Optional, Any, Tuple, Callable
from selenium import webdriver

class Bot(object):
    """
    Represents a d4v1d-Bot.

    ...

    Attributes
    ----------
    cookies : Dict[str, str]
        The cookies that define the bot's user session.
    sess : requests.Session
        The bot's session (the one, the cookies will be stored in; used for all requests)
    headers : Dict[str, str]
        The headers that should be used for all requests.
    user : models.User
        The bot's user account.
    timestamp : float
        A timestamp of when the bot was created.
    net : Optional[BotNet]
        The botnet the bot belongs to.
    requests : int
        Total number of requests the bot has made.
    _running : bool
        Whether or not the bot should keep fetching and completing new bot tasks.
    status : str
        What is the bot doing at the moment?

    Methods
    -------
    login()
        Opens a selenium window, allows the user to log in and stores the cookies.
    login_with(uname, passw)
        Signs in with the provided username and password using the Instagram private API.
    req(method, url)
        Uses the bot's session to request the given URL.
    start()
        Start the bot; starts fetching new tasks from botnet (separate thread). Won't do anything without a botnet.
    _run()
        Keeps fetching and completing new tasks from botnet.
    stop()
        Stop the bot; stops fetching new tasks (ends thread).
    """

    NO_TASK_TIMEOUT: int = 2

    @classmethod
    def ccookie(cls, c: Dict[Any, Any]) -> Dict[str, str]:
        """Converts a cookie from selenium to requests. Only keeps legal attributes."""
        allowed = [ 
            'version', 
            'name', 
            'value', 
            'port', 
            'port_specified', 
            'domain', 
            'domain_specified', 
            'domain_initial_dot', 
            'path', 
            'path_specified', 
            'secure', 
            'expires', 
            'discard', 
            'comment', 
            'comment_url', 
            'rest', 
            'rfc2109', 
        ]
        return { k: v for k, v in c.items() if k in allowed}

    @classmethod
    def gen_user_agent(cls) -> str:
        """Generates and returns a valid Instagram User-Agent string with the parameters defined in lib.api.params"""
        return 'Instagram {APP_VERSION} Android ({ANDROID_VERSION}/{ANDROID_RELEASE}; {PHONE_MANUFACTURER}; {PHONE_DEVICE}; {PHONE_MODEL}; {PHONE_DPI}; {PHONE_RESOLUTION}; {PHONE_CHIPSET}; en_US; {VERSION_CODE})'\
                .format(**params.USER_AGENT)

    @classmethod
    def gen_headers(cls, user_agent: Optional[str] = None) -> Dict[str, str]:
        """Generates and returns valid headers for a mobile Instagram client"""
        return {
            'User-Agent': user_agent or Bot.gen_user_agent(),
            'Connection': 'close',
            'Accept': '*/*',
            'Accept-Language': 'en-US',
            'Accept-Encoding': 'gzip, deflate',
            'X-IG-Capabilities': params.IG_CAPABILITIES,
            'X-IG-Connection-Type': 'WIFI',
            'X-IG-Connection-Speed': '{0:d}kbps'.format(random.randint(1000, 5000)),
            'X-IG-App-ID': params.APPLICATION_ID,
            'X-IG-Bandwidth-Speed-KBPS': '-1.000',
            'X-IG-Bandwidth-TotalBytes-B': '0',
            'X-IG-Bandwidth-TotalTime-MS': '0',
            'X-FB-HTTP-Engine': params.FB_HTTP_ENGINE,
        }

    @classmethod
    def seed(cls, *args: str) -> str:
        """Generate seed for certain Instagram requests"""
        m = hashlib.md5()
        m.update(b''.join([arg.encode() for arg in args]))
        return m.hexdigest()

    @classmethod
    def gen_device_id(cls, seed: str) -> str:
        """Generate device id for certain Instagram requests"""
        vol_seed = "12345"
        m = hashlib.md5()
        m.update(seed.encode() + vol_seed.encode())
        return 'android-{}'.format(m.hexdigest()[:16])

    @classmethod
    def gen_uuid(cls) -> str:
        """Generate a uuid"""
        return str(uuid.uuid4())

    @classmethod
    def gen_signature(cls, data: str) -> str:
        """Generates a signature for certain requests"""
        body = hmac.new(params.IG_SIG_KEY.encode(), data.encode(), hashlib.sha256).hexdigest() + '.' + urllib.parse.quote(data)
        return 'ig_sig_key_version={}&signed_body={}'.format(params.SIG_KEY_VERSION, body)

    @classmethod
    def get_user_by_id(cls, self: 'Bot', uid: int) -> models.User:
        """Gets an Instagram user via its pk (user-id)"""
        base.pause()
        res = self.req('get', urls.IINFO.format(uid)).json()['user']
        return models.User(res['pk'], res['username'], res['biography'], res['external_url'], res['full_name'], 
                           res['is_business'], res['is_private'], res['is_verified'], res['hd_profile_pic_url_info']['url'], 
                           res['follower_count'], res['following_count'], res)

    @classmethod
    def get_followers(cls, self: 'Bot', pk: int) -> List[int]:
        """Gets and stores all the followers the specified Instagram user has."""
        self.status = 'get_followers({})'.format(local.get_user_by_pk(pk).uname)
        fls = Bot._get_followers(self, pk)
        con, c = db.connect()
        lfls = list(map(lambda e: e[0], db.fetchall('SELECT fpk FROM fols WHERE tpk = ? AND last_seen IS NULL', pk, con=con)))
        for f in filter(lambda pf: pf not in fls, lfls):
            db.exec('UPDATE fols SET last_seen = ? WHERE fpk = ? AND tpk = ? AND last_seen IS NULL', datetime.datetime.now(), f, pk, con=con)
        for f in filter(lambda pf: pf not in lfls, fls):
            db.exec('INSERT INTO fols (fpk, tpk) VALUES (?, ?)', f, pk)
        db.close(con)
        return fls

    @classmethod
    def _get_followers(cls, self: 'Bot', pk: int, after: str = '') -> List[int]:
        """Gets all the followers the specified Instagram user has."""
        base.pause()
        res = self.req('get', urls.FOLLOWERS.format(json.dumps({
            'id': str(pk),
            'first': 24,
            'after': after,
        }))).json()
        if not res['status'] == 'ok':
            return []
        inf = res['data']['user']['edge_followed_by']
        return [
            *map(lambda u: int(u['node']['id']), inf['edges']),
            *(Bot._get_followers(self, pk, inf['page_info']['end_cursor']) if inf['page_info']['has_next_page'] else []),
        ]

    @classmethod
    def get_following(cls, self: 'Bot', pk: int) -> List[int]:
        """Gets and stores all the user ids the specified Instagram user follows"""
        self.status = 'get_following({})'.format(local.get_user_by_pk(pk).uname)
        fls = Bot._get_following(self, pk)
        con, c = db.connect()
        lfls = list(map(lambda e: e[0], db.fetchall('SELECT tpk FROM fols WHERE fpk = ? AND last_seen IS NULL', pk, con=con)))
        for f in filter(lambda pf: pf not in fls, lfls):
            db.exec('UPDATE fols SET last_seen = ? WHERE fpk = ? AND tpk = ? AND last_seen IS NULL', datetime.datetime.now(), pk, f, con=con)
        for f in filter(lambda pf: pf not in lfls, fls):
            db.exec('INSERT INTO fols (fpk, tpk) VALUES (?, ?)', pk, f)
        db.close(con)
        return fls

    @classmethod
    def _get_following(cls, self: 'Bot', pk: int, after: str = '') -> List[int]:
        """Gets all the user ids the specified Instagram user follows."""
        base.pause()
        res = self.req('get', urls.FOLLOWING.format(json.dumps({
            'id': str(pk),
            'first': 24,
            'after': after,
        }))).json()
        if not res['status'] == 'ok':
            return []
        inf = res['data']['user']['edge_follow']
        return [
            *map(lambda u: int(u['node']['id']), inf['edges']),
            *(Bot._get_following(self, pk, inf['page_info']['end_cursor']) if inf['page_info']['has_next_page'] else []),
        ]

    @classmethod
    def _get_media(cls, self: 'Bot', pk: int, after: str = '') -> None:
        pass

    def __init__(self, cookies: Dict[str, str] = {}, creds: Tuple[str, str] = (), net: Optional['BotNet'] = None) -> None:
        """
        Parameters
        ----------
        cookies : Dict[str, str]
            The cookies that define this bot user's session.
            Default is {} (a selenium window will open in that case).
        creds : Tuple[str, str]
            A username/password combination; the bot will login using this (if provided). [NOT-WORKING-AT-THE-MOMENT]
        """
        self.sess: req.Session = req.Session()
        self.headers: Dict[str, str] = Bot.gen_headers()
        self.cookies: Dict[str, str] = cookies
        if not self.cookies:
            if creds:
                self.login_with(*creds)
            else:
                self.login()
        for c in self.cookies:
            self.sess.cookies.set(**self.cookies[c])
        self.net: Optional[BotNet] = net
        self.requests: int = 0
        self.user: models.User = Bot.get_user_by_id(self, self.sess.cookies.get('ds_user_id'))
        self.timestamp: float = time.time()
        self._running: bool = False
        self.status: str = 'stopped'

    def login(self) -> None:
        """Opens a selenium window, asks the user to log in and saves the cookies."""
        driver = webdriver.Firefox()
        driver.get(urls.N_LOGIN)
        curl = driver.current_url
        while driver.current_url == curl:
            time.sleep(1)
        driver.minimize_window()
        yn = input('Are you done [y/n]? ')
        if not yn.lower() == 'y':
            driver.maximize_window()
            input('Press [ENTER] when you\'re done ... ')
        cookies = driver.get_cookies()
        driver.close()
        self.cookies = { c['name']: c for c in map(Bot.ccookie, cookies) }

    def login_with(self, uname: str, passw: str) -> None:
        """[NOT-WORKING-AT-THE-MOMENT] Signs in via the Instagram private API."""
        data = json.dumps({
            'jazoest': str(random.randint(22000, 22999)),
            'country_codes': '[{"country_code":"1","source":["default"]}]',
            'phone_id': Bot.gen_uuid(),
            '_csrftoken': public.get_csrftoken(),
            'username': uname,
            'adid': '',
            'guid': Bot.gen_uuid(),
            'device_id': Bot.gen_device_id(Bot.seed(uname, uname)),
            'google_tokens': '[]',
            'password': passw,
            'login_attempt_count': '1',
        })
        print(data)
        data = Bot.gen_signature(data)
        print(data)
        res = self.req('post', urls.LOGIN, data=data)
        print(res)
        print(res.text)
        import os
        os._exit(0)

    def req(self, method: str, url: str) -> req.Response:
        self.requests += 1
        return self.sess.request(method, url, headers=self.headers)

    def start(self) -> None:
        """Start the bot; starts fetching new tasks from botnet (separate thread). Won't do anything without a botnet."""
        if not self.net:
            return
        self.status = 'starting'
        t = threading.Thread(target=self._run)
        t.start()

    def _run(self) -> None:
        """Keeps fetching and completing new tasks from botnet."""
        self._running = True
        while self._running:
            self.status = 'idling'
            t = self.net.next_task(self)
            if not t:
                time.sleep(Bot.NO_TASK_TIMEOUT)
                continue
            t.callback(t.target(self, *t.args, **t.kwargs))

    def stop(self) -> None:
        """Stop the bot; stops fetching new tasks (ends thread)."""
        self._running = False
        self.status = 'stopped'

    def __str__(self) -> str:
        return 'Bot [{}#{}] ... {}'.format(self.user.uname, self.user.pk, self.status)

    def __eq__(self, other):
        if not isinstance(other, Bot):
            return False
        return self.user.pk == other.user.pk

class BotTask(object):
    """
    Represents a task for a d4v1d-bot.

    ...

    Attributes
    ----------
    target : Callable[..., None]
        The task's target function, the one the bot should execute.
    prereq : Callable[[Bool], bool]
        The task's prerequisite.
    args : List[Any]
        Positional arguments for the target function.
    kwargs : Dict[str, Any]
        Keyword arguments for the target function.
    callback : Callable[Any, None]
        Will be called upon completion, with the result - if any.
    cant : Set[Bot]
        Set of bots that cannot complete the task.

    Methods
    -------
    nope(bot)
        Add bot the can't complete list.
    """

    def __init__(self, target: Callable[..., None], prereq: Callable[[Bot, int], bool], 
                 args: List[Any], kwargs: Dict[str, Any], callback: Callable[..., None]) -> None:
        self.target: Callable[..., None] = target
        self.prereq: Callable[[Bot, int], bool] = prereq
        self.args: List[Any] = args
        self.kwargs: Dict[str, Any] = kwargs
        self.callback: Callable[..., None] = callback
        self.cant: List[Bot] = []

    def nope(self, bot: Bot):
        """Add bot the can't complete list"""
        self.cant.append(bot)

    def __str__(self) -> str:
        return 'BotTask [{}]'.format(self.target.__name__)

class BotTaskPrerequisite(object):
    """
    Multiple prerequisites for BotTasks.
    """

    @classmethod
    def everyone(cls, pk: int) -> Callable[[Bot], bool]:
        return lambda bot: True

    @classmethod
    def following(cls, pk: int) -> Callable[[Bot], bool]:
        return lambda bot: pk in local.get_following(bot.user.pk)

class BotNet(object):
    """
    Represents a collection of d4v1d-Bots - a BotNet.

    ...

    Attributes
    ----------
    bots : Set[Bot]
        Set containing all bots in the botnet.
    q : List[BotTask]
        Tasks for the bots to complete.
    qsem : threading.Semaphore
        Semaphore for synchronized q access.

    Methods
    -------
    load(fname)
        Loads bots from a cookie store.
    store(fname)
        Stores bots to a cookie store.
    add(bot)
        Adds a bot to the botnet.
    """

    def __init__(self, bots: List[Bot] = [], nload: bool = False) -> None:
        """
        Parameters
        ----------
        bots : List[Bot]
            The initial list of bots.
        nload : bool
            Don't load past bots from the cookie store.
        """
        self.bots: List[Bot] = bots
        self.q: List[BotTask] = []
        self.qsem: threading.Semaphore = threading.Semaphore()
        if not nload:
            self.load()

    def load(self, fname: str = os.path.join(params.TMP_PATH, 'cookies.json')) -> None:
        """Loads previously used bots from the cookie store."""
        if not os.path.exists(fname):
            return
        with open(fname, 'r') as f:
            bs = json.load(f)
            pks = list(map(lambda b: b.user.pk, self.bots))
            ext = [ Bot(cookies=b['cookies'], net=self) for b in bs if time.time() - b['timestamp'] < params.BOT_TIMEOUT and b['pk'] not in pks ]
            self.bots.extend(ext)
            for b in ext:
                b.start()
            if len(ext) == 0:
                print(' No new bots were added to the botnet ... ')
                return
            print(' Extended botnet by {} bots ... '.format(len(ext)))

    def store(self, fname: str = os.path.join(params.TMP_PATH, 'cookies.json')) -> None:
        """Stores current bot list to the cookie store."""
        if not os.path.isdir(os.path.dirname(fname)):
            os.path.makedirs(os.path.dirname(fname))
        with open(fname, 'w') as f:
            json.dump([ dict(timestamp=b.timestamp, pk=b.user.pk, cookies=b.cookies) for b in self.bots ], f)

    def add(self, bot: Optional[Bot] = None) -> None:
        """Adds a new bot to the botnet"""
        b = bot or Bot(net=self)
        self.bots.append(b)
        self.store()
        b.start()

    def stop(self) -> None:
        for b in self.bots:
            b.stop()

    def wait_till_done(self) -> None:
        while self.q:
            if not any(map(lambda b: b._running, self.bots)):
                break
            time.sleep(2)
        self.stop()

    def next_task(self, bot: Bot) -> Optional[BotTask]:
        ft = None
        ri = []
        self.qsem.acquire()
        for i, t in enumerate(self.q):
            if t.prereq(bot):
                ft = t
                ri.append(i)
                break
            else:
                t.nope(bot)
            if self.bots.issubset(t.cant):
                ri.append(i)
        for i in reversed(ri):
            del self.q[i]
        self.qsem.release()
        return ft

    def get_followers(self, uname: str, *unames: str) -> None:
        """Adds a task for one of the bots to get all followers of the given user."""
        for u in [uname, *unames]:
            user = public.get_user(u)
            prereq = BotTaskPrerequisite.following(user.pk) if user.private else BotTaskPrerequisite.everyone(user.pk)
            self.q.append(BotTask(Bot.get_followers, prereq, [user.pk,], {}, lambda fls: None))

    def get_following(self, uname: str, *unames: str) -> None:
        """Adds a task for one of the bots to get all following of the given user."""
        for u in [uname, *unames]:
            user = public.get_user(u)
            prereq = BotTaskPrerequisite.following(user.pk) if user.private else BotTaskPrerequisite.everyone(user.pk)
            self.q.append(BotTask(Bot.get_following, prereq, [user.pk,], {}, lambda fls: None))