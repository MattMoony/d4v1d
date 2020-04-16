"""
All wrappers for the private API are implemented here. (private endpoints --> need to be authenticated, maybe authorized)
"""

from lib import models
from lib.api import urls, params, base, public
import time, random, uuid, hmac, json, hashlib, os
import requests as req
import six.moves.urllib as urllib
from typing import List, Dict, Optional, Any, Tuple
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

    Methods
    -------
    login()
        Opens a selenium window, allows the user to log in and stores the cookies.
    login_with(uname, passw)
        Signs in with the provided username and password using the Instagram private API.
    get_user_by_id(uid)
        Will retrieve an Instagram user via its pk (user-id).
    """

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
        m = hashlib.md5()
        m.update(b''.join([arg.encode() for arg in args]))
        return m.hexdigest()

    @classmethod
    def gen_device_id(cls, seed: str) -> str:
        vol_seed = "12345"
        m = hashlib.md5()
        m.update(seed.encode() + vol_seed.encode())
        return 'android-{}'.format(m.hexdigest()[:16])

    @classmethod
    def gen_uuid(cls) -> str:
        return str(uuid.uuid4())

    @classmethod
    def gen_signature(cls, data: str) -> str:
        body = hmac.new(params.IG_SIG_KEY.encode(), data.encode(), hashlib.sha256).hexdigest() + '.' + urllib.parse.quote(data)
        return 'ig_sig_key_version={}&signed_body={}'.format(params.SIG_KEY_VERSION, body)

    def __init__(self, cookies: Dict[str, str] = {}, creds: Tuple[str, str] = ()) -> None:
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
        self.user: models.User = self.get_user_by_id(self.sess.cookies.get('ds_user_id'))
        self.timestamp: float = time.time()

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
        res = self.sess.post(urls.LOGIN, headers=self.headers, data=data)
        print(res)
        print(res.text)
        import os
        os._exit(0)

    def get_user_by_id(self, uid: int) -> models.User:
        """Gets an Instagram user via its pk (user-id)"""
        base.pause()
        res = self.sess.get(urls.IINFO.format(uid), headers=self.headers).json()['user']
        return models.User(res['pk'], res['username'], res['biography'], res['external_url'], res['full_name'], 
                           res['is_business'], res['is_private'], res['is_verified'], res['hd_profile_pic_url_info']['url'], 
                           res['follower_count'], res['following_count'], res)

    def __str__(self) -> str:
        return 'Bot [{}#{}]'.format(self.user.uname, self.user.pk)

class BotNet(object):
    """
    Represents a collection of d4v1d-Bots - a BotNet.

    ...

    Attributes
    ----------
    bots : List[Bot]
        List containing all bots in the botnet.

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
        self.bots = bots
        if not nload:
            self.load()

    def load(self, fname: str = os.path.join(params.TMP_PATH, 'cookies.json')) -> None:
        """Loads previously used bots from the cookie store."""
        if not os.path.exists(fname):
            return
        with open(fname, 'r') as f:
            bs = json.load(f)
            pks = list(map(lambda b: b.user.pk, self.bots))
            ext = [ Bot(cookies=b['cookies']) for b in bs if time.time() - b['timestamp'] < params.BOT_TIMEOUT and b['pk'] not in pks ]
            self.bots.extend(ext)
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
        b = bot or Bot()
        if b.user.pk in list(map(lambda b: b.user.pk, self.bots)):
            return
        self.bots.append(b)
        self.store()