import os, json, math, time, datetime
import requests as req
import plotly.graph_objects as go
from queue import Queue
from lib import api, urls, login, params

CACHE_PATH = 'cache.json'
TIMEOUT = 60*60*12

class UNode(object):
    def __init__(self, id, fr):
        self.id = id
        self.fr = fr

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash((self.id, self.fr))

class Bot(object):
    def __init__(self, cache=True):
        if not os.path.isdir(os.path.join(params.TMP_PATH, os.path.dirname(CACHE_PATH))):
            os.mkdir(os.path.join(params.TMP_PATH, os.path.dirname(CACHE_PATH)))
        if cache and os.path.isfile(os.path.join(params.TMP_PATH, CACHE_PATH)):
            with open(os.path.join(params.TMP_PATH, CACHE_PATH)) as f:
                try:
                    tmp = json.load(f)
                    if time.time()-tmp['timestamp'] < TIMEOUT:
                        self.cookies = tmp['cookies']
                        print(' Loading from cache ({}) ... '.format(os.path.join(params.TMP_PATH, CACHE_PATH)))
                except Exception:
                    pass
        if 'cookies' not in dir(self):
            self.cookies = login.login()
            if self.cookies:
                with open(os.path.join(params.TMP_PATH, CACHE_PATH), 'w') as f:
                    json.dump({ 'timestamp': time.time(), 'cookies': self.cookies, }, f)
        self.session = req.Session()
        for c in self.cookies:
            self.session.cookies.set(**self.cookies[c])
        self.headers = api.gen_headers()
        self.user = api.get_user_info_by_id(self.session.cookies.get('ds_user_id'), headers=self.headers)['user']

    # -- USEABLE -------------------------------------------------------------- #

    def get_following(self, userid=None, nxmi=None):
        if not userid:
            userid = self.cookies['ds_user_id']['value']
        res = self.session.get(urls.FOLLOWING.format(userid)+('?max_id={}'.format(nxmi) if nxmi else ''), headers=self.headers).json()
        if 'big_list' in res.keys() and res['big_list']:
            return [*self.get_following(userid, res['next_max_id']), *res['users']]
        return res['users'] if 'users' in res.keys() else []
        
    def get_followers(self, userid=None, nxmi=None):
        if not userid:
            userid = self.cookies['ds_user_id']['value']
        res = self.session.get(urls.FOLLOWERS.format(userid)+('?max_id={}'.format(nxmi) if nxmi else ''), headers=self.headers).json()
        if 'big_list' in res.keys() and res['big_list']:
            return [*self.get_followers(userid, res['next_max_id']), *res['users']]
        return res['users'] if 'users' in res.keys() else []

    def get_follower_nodes(self, username, d=2):
        if d == 0:
            return ([], [], [], [], [])
        if api.get_follower_count(username, headers=self.headers) > 500:
            return ([], [], [], [], [])
        print('[*] Indexing {} ... '.format(username))

        userid = api.get_userid(username, headers=self.headers)
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
        to = api.get_userid(to)
        print(to)
        if not fr:
            fr = self.cookies['ds_user_id']['value']
        else:
            fr = api.get_userid(fr, headers=self.headers)
        q = Queue()
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
            path.append(api.get_username(c.id, headers=self.headers))
            c = c.fr
        return list(reversed(path))