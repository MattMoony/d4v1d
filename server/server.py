import os, threading, json, logging
from flask import Flask, request, Response, send_from_directory, render_template
from flup.server.fcgi import WSGIServer
import requests as req
from lib import params, misc, cache

LOG = logging.getLogger('werkzeug')
LOG.disabled = True
CONF = {}
PUBLIC = os.path.abspath(os.path.join(params.SRV_PATH, 'public'))
TEMPLT = os.path.abspath(os.path.join(params.SRV_PATH, 'templates'))

if not os.path.isfile(os.path.join(params.SRV_PATH, 'config/conf.json')):
    misc.print_err('server', 'Missing configuration file! Supposed to be at "{}" ... '.format(os.path.abspath(os.path.join(params.SRV_PATH, 'config/conf.json'))))
    os._exit(1)
with open(os.path.join(params.SRV_PATH, 'config/conf.json'), 'r') as f:
    CONF = json.load(f)

__app = Flask(__name__, static_url_path='/', static_folder=PUBLIC, template_folder=TEMPLT)
__app.logger.disabled = True
__server = None

def not_scraped():
    return Response(json.dumps(dict(msg='Not scraped!')), mimetype='application/json')

@__app.route('/')
@__app.route('/index.html')
def index():
    return render_template('index.html', users=[d for d in os.listdir(params.TMP_PATH) if os.path.isdir(os.path.join(params.TMP_PATH, d))])

@__app.route('/api/followers/<uname>')
def followers(uname):
    # upath = os.path.join(params.TMP_PATH, uname)
    # if not os.path.isdir(upath):
    #     return not_scraped()
    # ogs = [d for d in os.listdir(upath) if os.path.isdir(os.path.join(upath, d)) and d.startswith('o') and os.path.isfile(os.path.join(upath, d, 'followers.json'))]
    # if not ogs:
    #     return Response(json.dumps(dict(msg='Not scraped!')), mimetype='application/json')
    # ogs.sort()
    # with open(os.path.join(upath, ogs[-1], 'followers.json'), 'r') as f:
    #     return Response('{{"success":true,"followers":{}}}'.format(f.read()), mimetype='application/json')
    fols = cache.load_followers(uname)
    if not fols:
        return not_scraped()
    return Response('{{"success":true,"followers":{}}}'.format(json.dumps(fols)), mimetype='application/json')

@__app.route('/api/following/<uname>')
def following(uname):
    # upath = os.path.join(params.TMP_PATH, uname)
    # if not os.path.isdir(upath):
    #     return not_scraped()
    # igs = [d for d in os.listdir(upath) if os.path.isdir(os.path.join(upath, d)) and d.startswith('i') and os.path.isfile(os.path.join(upath, d, 'following.json'))]
    # if not igs:
    #     return not_scraped()
    # igs.sort()
    # with open(os.path.join(upath, igs[-1], 'following.json'), 'r') as f:
    #     return Response('{{"success":true,"following":{}}}'.format(f.read()), mimetype='application/json')
    fols = cache.load_following(uname)
    if not fols:
        return not_scraped()
    return Response('{{"success":true,"following":{}}}'.format(json.dumps(fols)), mimetype='application/json')

@__app.route('/shut', methods=['POST',])
def shut():
    request.environ.get('werkzeug.server.shutdown')()

def run():
    global __server
    if not __server:
        __server = threading.Thread(target=__app.run, kwargs=dict(host=CONF['host'],port=CONF['port']))
        __server.start()

def stop():
    if __server:
        req.post('http://{}:{}/shut'.format(CONF['host'], CONF['port']))