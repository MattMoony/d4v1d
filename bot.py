import os, json, math, login, random, datetime
import requests as req
from queue import Queue
from random import randint
import plotly.graph_objects as go

BASE_PATH = os.path.abspath(os.path.dirname(__file__))

class SetQueue(Queue):
    def _init(self, maxsize):
        self.queue = set()
    def _put(self, item):
        self.queue.add(item)
    def _get(self):
        return self.queue.pop()

class URLs(object):
    login = 'https://i.instagram.com/api/v1/accounts/login/'
    followers = 'https://i.instagram.com/api/v1/friendships/{}/followers/'
    following = 'https://i.instagram.com/api/v1/friendships/{}/following/'
    media = 'https://i.instagram.com/api/v1/feed/user/{}/'
    info = 'https://i.instagram.com/api/v1/users/{}/info/'

class Config(object):
    IG_SIG_KEY = '19ce5f445dbfd9d29c59dc2a78c616a7fc090a8e018b9267bc4240a30244c53b'
    IG_CAPABILITIES = '3brTvw=='
    SIG_KEY_VERSION = '4'
    APP_VERSION = '76.0.0.15.395'
    APPLICATION_ID = '567067343352427'
    FB_HTTP_ENGINE = 'Liger'
    
    ANDROID_VERSION = 24
    ANDROID_RELEASE = '7.0'
    PHONE_MANUFACTURER = 'samsung'
    PHONE_DEVICE = 'SM-G930F'
    PHONE_MODEL = 'herolte'
    PHONE_DPI = '640dpi'
    PHONE_RESOLUTION = '1440x2560'
    PHONE_CHIPSET = 'samsungexynos8890'
    VERSION_CODE = '138226743'

class API(object):
    @staticmethod
    def get_user_info(username):
        return req.get('https://www.instagram.com/{}/?__a=1'.format(username)).json()

    @staticmethod
    def get_userid(username):
        return API.get_user_info(username)['graphql']['user']['id']

    @staticmethod
    def get_followers(username):
        return API.get_user_info(username)['graphql']['user']['edge_followed_by']['count']

    @staticmethod
    def get_following(username):
        return API.get_user_info(username)['graphql']['user']['edge_follow']['count']

class UNode(object):
    def __init__(self, id, fr):
        self.id = id
        self.fr = fr

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash((self.id, self.fr))

class Bot(object):
    urls = URLs()
    conf = Config()

    def __init__(self):
        if not os.path.isfile(os.path.join(BASE_PATH, 'cookies.json')):
            self.cookies = login.login()
            with open(os.path.join(BASE_PATH, 'cookies.json'), 'w') as f:
                json.dump(self.cookies, f)
        else:
            with open(os.path.join(BASE_PATH, 'cookies.json'), 'r') as f:
                self.cookies = json.load(f)
        self.session = req.Session()
        for c in self.cookies:
            self.session.cookies.set(**self.cookies[c])
        
        self.user_agent = self.gen_user_agent()
        self.headers = self.gen_headers()

    # -- USEABLE -------------------------------------------------------------- #

    def get_followers(self, userid=None, nxmi=None):
        if not userid:
            userid = self.cookies['ds_user_id']['value']
        res = self.session.get(self.urls.followers.format(userid)+('?max_id={}'.format(nxmi) if nxmi else ''), headers=self.headers).json()
        if 'big_list' in res.keys() and res['big_list']:
            return [*self.get_followers(userid, res['next_max_id']), *res['users']]
        return res['users'] if 'users' in res.keys() else []

    def get_follower_nodes(self, username, d=2):
        if d == 0:
            return ([], [], [], [], [])
        if API.get_followers(username) > 500:
            return ([], [], [], [], [])
        print('[*] Indexing {} ... '.format(username))

        userid = API.get_userid(username)
        followers = self.get_followers(userid)

        if len(followers) == 0:
            return ([], [], [], [], [])

        phi = 2*math.pi/len(followers)
        r = [20, 30, 40, 50]
        node_x = [0]
        node_y = [0]
        edge_x = []
        edge_y = []
        node_text = [username]

        for i, _ in enumerate(followers):
            node_x.append(math.cos(i*phi)/r[i%len(r)])
            node_y.append(math.sin(i*phi)/r[i%len(r)])
            edge_x.append(0)
            edge_y.append(0)        
            edge_x.append(node_x[-1])
            edge_y.append(node_y[-1])
            edge_x.append(None)
            edge_y.append(None)

        for f in followers:
            fnx, fny, fex, fey, ntxt = self.get_follower_nodes(f['username'], d-1)
            node_x = [*node_x, *fnx]
            node_y = [*node_y, *fny]
            edge_x = [*edge_x, *fex]
            edge_y = [*edge_y, *fey]
            node_text = [*node_text, *ntxt]

        return (node_x, node_y, edge_x, edge_y, node_text)

    def plot_followers(self, username):
        node_x, node_y, edge_x, edge_y, node_text = self.get_follower_nodes(username)

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#D2C2FF'),
            hoverinfo='none',
            mode='lines'
        )

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='text',
            hoverinfo='text',
            text=[],
            marker=dict(
                showscale=True,
                colorscale='Electric',
                reversescale=True,
                color=[],
                size=10,
                line_width=2
            )
        )

        node_trace.text = node_text

        fig = go.Figure(data=[edge_trace, node_trace],
                     layout=go.Layout(
                        title='{}\'{} followers'.format(username, 's' if not username.endswith('s') else ''),
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40),
                        annotations=[ dict(
                            text='<i>{}</i>'.format(datetime.datetime.now().isoformat()),
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002 ) ],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                        )
        fig.show()

    def shortest_path(self, to, fr=None):
        to = API.get_userid(to)
        print(to)
        if not fr:
            fr = self.cookies['ds_user_id']['value']
        else:
            fr = API.get_userid(fr)
        q = SetQueue()
        q.put(UNode(fr, -1))
        while not q.empty():
            c = q.get()
            print('Indexing {} ...'.format(c.id))
            if c.id == to:
                break
            for f in self.get_followers(c.id):
                print(f)
                if not f in q.queue:
                    q.put(UNode(f['pk'], c))
        path = []
        while c.fr != -1:
            path.append(self.get_username(c.id))
            c = c.fr
        return list(reversed(path))

    # -- UTILS ---------------------------------------------------------------- #

    def gen_headers(self):
        return {
            'User-Agent': self.user_agent,
            'Connection': 'close',
            'Accept': '*/*',
            'Accept-Language': 'en-US',
            'Accept-Encoding': 'gzip, deflate',
            'X-IG-Capabilities': self.conf.IG_CAPABILITIES,
            'X-IG-Connection-Type': 'WIFI',
            'X-IG-Connection-Speed': '{0:d}kbps'.format(random.randint(1000, 5000)),
            'X-IG-App-ID': self.conf.APPLICATION_ID,
            'X-IG-Bandwidth-Speed-KBPS': '-1.000',
            'X-IG-Bandwidth-TotalBytes-B': '0',
            'X-IG-Bandwidth-TotalTime-MS': '0',
            'X-FB-HTTP-Engine': self.conf.FB_HTTP_ENGINE,
        }

    def gen_user_agent(self):
        return 'Instagram {} Android ({}/{}; {}; {}; {}; {}; {}; {}; en_US; {})'\
                .format(self.conf.APP_VERSION, self.conf.ANDROID_VERSION, self.conf.ANDROID_RELEASE,
                        self.conf.PHONE_MANUFACTURER, self.conf.PHONE_DEVICE, self.conf.PHONE_MODEL,
                        self.conf.PHONE_DPI, self.conf.PHONE_RESOLUTION, self.conf.PHONE_CHIPSET, 
                        self.conf.VERSION_CODE)

    def gen_rank_token(self, uid):
        ptrn = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'
        return '{}_{}'.format(uid, ''.join([ptrn[i] if ptrn[i] not in ['x', 'y'] else str(randint(0,16) & 0x3 if ptrn[i] == 'x' else randint(0,16) & 0x8) for i in range(len(ptrn))]))

    def get_user_info_by_id(self, uid):
        return req.get(self.urls.info.format(uid), headers=self.headers).json()

    def get_username(self, uid):
        return self.get_user_info_by_id(uid)['user']['username']

if __name__ == '__main__':
    bot = Bot()
    with open('cache.json', 'w') as f:
        json.dump(bot.get_followers(), f)
    print(bot.shortest_path('weinstein.cookies'))