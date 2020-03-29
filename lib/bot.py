import os, json, time, threading
import requests as req
from queue import Queue
from lib import api, urls, login, params, misc, cache

CACHE_PATH = 'cache.json'
TIMEOUT = 60*60*12

class UNode(object):
    def __init__(self, id, uname, to, fr):
        self.id = id
        self.uname = uname
        self.to = to
        self.fr = fr

    def __eq__(self, other):
        if type(other) == UNode:
            return self.id == other.id
        return self.id == other['id']

    def __hash__(self):
        return hash((self.id, self.fr))

class Bot(object):
    def __init__(self, cookies={}):
        self.cookies = cookies
        if not self.cookies:
            self.cookies = login.login()
            # if self.cookies:
            #     with open(os.path.join(params.TMP_PATH, CACHE_PATH), 'w') as f:
            #         json.dump({ 'timestamp': time.time(), 'cookies': self.cookies, }, f)
        self.session = req.Session()
        for c in self.cookies:
            self.session.cookies.set(**self.cookies[c])
        self.timestamp = time.time()
        self.headers = api.gen_headers()
        self.user = api.get_user_info_by_id(self.session.cookies.get('ds_user_id'), headers=self.headers)['user']

    # -- USEABLE -------------------------------------------------------------- #

    def get_followingr(self, userid, nxmi=None):
        res = self.session.get(urls.FOLLOWING.format(json.dumps({
            'id': userid,
            'first': 50,
            'after': nxmi,
        })), headers=self.headers).json()
        if res['status'] != 'ok':
            misc.print_wrn('get_followingr({})'.format(userid), json.dumps(res))
            return []
        res = res['data']['user']['edge_follow']
        if res['page_info']['has_next_page']:
            return [*self.get_followingr(userid, res['page_info']['end_cursor']), *list(map(lambda e: e['node'], res['edges']))]
        return list(map(lambda e: e['node'], res['edges']))

    def get_following(self, username, dcache=False):
        fols = self.get_followingr(api.get_userid(username))
        # if len(fols) == 0:
        #     misc.print_wrn('get_following({})'.format(username), 'No following found ... (maybe private) ')
        if not dcache:
            # outd = os.path.abspath(os.path.join(params.TMP_PATH, '{}/i{}'.format(username, str(time.time()))))
            # if not os.path.isdir(outd):
            #     os.makedirs(outd)
            # with open(os.path.join(outd, 'following.json'), 'w') as f:
            #     json.dump(fols, f, indent=4, sort_keys=True)
            cache.store_following(username, fols)
        return fols

    def get_followersr(self, userid, nxmi=None):
        res = self.session.get(urls.FOLLOWERS.format(json.dumps({
            'id': userid,
            'first': 50,
            'after': nxmi,
        })), headers=self.headers).json()
        if res['status'] != 'ok':
            misc.print_wrn('get_followersr({})'.format(userid), json.dumps(res))
            return []
        res = res['data']['user']['edge_followed_by']
        if res['page_info']['has_next_page']:
            return [*self.get_followersr(userid, res['page_info']['end_cursor']), *list(map(lambda e: e['node'], res['edges']))]
        return list(map(lambda e: e['node'], res['edges']))

    def get_followers(self, username, dcache=False):
        fols = self.get_followersr(api.get_userid(username))
        # if len(fols) == 0:
        #     misc.print_wrn('get_followers({})'.format(username), 'No followers found ... (maybe private) ')
        if not dcache:
            # outd = os.path.abspath(os.path.join(params.TMP_PATH, '{}/o{}'.format(username, str(time.time()))))
            # if not os.path.isdir(outd):
            #     os.makedirs(outd)
            # with open(os.path.join(outd, 'followers.json'), 'w') as f:
            #     json.dump(fols, f, indent=4, sort_keys=True)
            cache.store_followers(username, fols)
        return fols

    def shortest_path(self, to, fr):
        q = Queue()
        q.put(UNode(api.get_userid(fr, headers=self.headers), fr, True, UNode(-1,'',True,None)))
        past = []
        found = False
        print(' ', end='')
        while not q.empty() and not found:
            c = q.get()
            past.append(c)
            print('. ', end='')
            api.pause()
            for f in self.get_followers(c.uname):
                if f['username'] == to:
                    found = True
                    c = UNode(f['id'], f['username'], False, c)
                    break
                if not f in q.queue and not f in past:
                    q.put(UNode(f['id'], f['username'], False, c))
            for f in self.get_following(c.uname):
                if f['username'] == to:
                    found = True
                    c = UNode(f['id'], f['username'], True, c)
                    break
                if not f in q.queue and not f in past:
                    q.put(UNode(f['id'], f['username'], True, c))
        print()
        path = []
        while c.fr != UNode(-1,'',True,None):
            path.append((c.to, c.uname))
            c = c.fr
        path.append((c.to, c.uname))
        return list(reversed(path))

class BotGroup(object):
    def __init__(self, cache=True):
        if not os.path.isdir(os.path.join(params.TMP_PATH, os.path.dirname(CACHE_PATH))):
            os.mkdir(os.path.join(params.TMP_PATH, os.path.dirname(CACHE_PATH)))
        self._bots = []
        if cache and os.path.isfile(os.path.join(params.TMP_PATH, CACHE_PATH)):
            with open(os.path.join(params.TMP_PATH, CACHE_PATH)) as f:
                try:
                    tmp = json.load(f)
                    print(' Loading from cache ({}) ... '.format(os.path.join(params.TMP_PATH, CACHE_PATH)))
                    for b in tmp:
                        if time.time() - b['timestamp'] < TIMEOUT:
                            self._bots.append(Bot(cookies=b['cookies']))
                except Exception:
                    pass

    def store(self, cpath=CACHE_PATH):
        with open(os.path.join(params.TMP_PATH, cpath)) as f:
            json.dump(map(lambda b: dict(timestamp=b.timestamp, cookies=b.cookies)), f)

    def add(self, bot=None):
        if isinstance(bot, Bot):
            self._bots.append(bot)
        else:
            self._bots.append(Bot())
        self.store()

    def _init(self):
        ts = []
        for b in self._bots:
            t = threading.Thread(target=b.get_followers, args=(b.user['username'],))
        for t in ts:
            t.join()