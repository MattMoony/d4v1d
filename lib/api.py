import random, time, os, json
import requests as req
from lib import params, urls, misc

SAFE_PAUSE = 10

    # -- FUNCTIONS -------------------------------------------------------------------------------------------- #

def get_user_info(username, headers={}):
    return req.get(urls.PUBLIC_INFO.format(username), headers=headers or gen_headers()).json()

def get_user_overview(username, **kwargs):
    res = get_user_info(username, **kwargs)['graphql']['user']
    return {
        'id': res['id'],
        'username': username,
        'full_name': res['full_name'],
        'external_url': res['external_url'],
        'followers': res['edge_followed_by']['count'],
        'following': res['edge_follow']['count'],
        'posts': res['edge_owner_to_timeline_media']['count'],
        'is_private': res['is_private'],
        'is_verified': res['is_verified'],
        # 'biography': res['biography'],
        # 'profile_pic_url_hd': res['profile_pic_url_hd'],
        # 'saved_media': res['edge_saved_media']['count'],
        # 'collections': res['edge_media_collections']['count'],
        # 'is_business_account': res['is_business_account'],
        # 'is_joined_recently': res['is_joined_recently'],
        # 'business_category_name': res['business_category_name'],
        # 'overall_category_name': res['overall_category_name'],
        # 'connected_fb_page': res['connected_fb_page'],
    }

def get_userid(username, **kwargs):
    return get_user_info(username, **kwargs)['graphql']['user']['id']

def get_follower_count(username, **kwargs):
    return get_user_info(username, **kwargs)['graphql']['user']['edge_followed_by']['count']

def get_following(username, **kwargs):
    return get_user_info(username, **kwargs)['graphql']['user']['edge_follow']['count']

def get_user_info_by_id(uid, headers={}):
    pause()
    uri = urls.INFO.format(uid)
    res = req.get(uri, headers=headers or gen_headers())
    return res.json()

def get_username(uid, **kwargs):
    return get_user_info_by_id(uid, **kwargs)['user']['username']

def pause(pause=SAFE_PAUSE):
    time.sleep(pause)

    # -- HELPERS -------------------------------------------------------------------------------------------- #
    
def gen_headers(user_agent=None):
    return {
        'User-Agent': user_agent or gen_user_agent(),
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

def gen_user_agent():
    return 'Instagram {} Android ({}/{}; {}; {}; {}; {}; {}; {}; en_US; {})'\
            .format(params.APP_VERSION, params.ANDROID_VERSION, params.ANDROID_RELEASE,
                    params.PHONE_MANUFACTURER, params.PHONE_DEVICE, params.PHONE_MODEL,
                    params.PHONE_DPI, params.PHONE_RESOLUTION, params.PHONE_CHIPSET, 
                    params.VERSION_CODE)

def gen_rank_token(uid):
    ptrn = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'
    return '{}_{}'.format(uid, ''.join([ptrn[i] if ptrn[i] not in ['x', 'y'] else str(random.randint(0,16) & 0x3 if ptrn[i] == 'x' else random.randint(0,16) & 0x8) for i in range(len(ptrn))]))

def down_img(node, dest, sess=None, shc='', sffx=''):
    if not sess:
        sess = req.Session()
    if 'shortcode' not in node.keys():
        node['shortcode'] = shc
    p = os.path.abspath(os.path.join(dest, '{}{}.{}'.format(node['shortcode'], sffx, 'mp4' if node['is_video'] else 'jpg')))
    print(' Getting "{}" --> "{}"'.format(node['shortcode'], p))
    try:
        with open(p, 'wb') as f:
            if node['is_video']:
                r = sess.get(node['video_url'])
                for ch in r.iter_content(chunk_size=255):
                    if ch:
                        f.write(ch)        
            else:
                f.write(sess.get(node['display_url']).content)
    except Exception as err:
        misc.print_wrn('get', 'Failed to retrieve post "{}" ... '.format(node['shortcode']))
        misc.print_wrn('get', str(err))

def get_media(username, dest=None, sess=None):
    userid = get_userid(username)
    variables = {
        'id': userid,
        'first': 50,
        'after': None
    }
    if not dest:
        dest = os.path.abspath(os.path.join(params.TMP_PATH, '{}/m{}'.format(username, str(time.time()))))
    loggedin = True
    if not sess:
        sess = req.Session()
        loggedin = False
    while True:
        res = sess.get(urls.MEDIA.format(json.dumps(variables))).json()
        if res['status'] != 'ok':
            break
        res = res['data']['user']['edge_owner_to_timeline_media']
        if len(res['edges']) == 0:
            misc.print_wrn('get', 'No media found! Maybe the account is private? {}'.format('' if loggedin else '(sign in and try again)'))
            return
        if not os.path.isdir(dest):
            try:
                os.makedirs(dest)
            except Exception:
                misc.print_wrn('get', 'Couldn\'t create directory "{}" --> aborting ... '.format(dest))
                return
        for e in res['edges']:
            if 'edge_sidecar_to_children' in e['node'].keys():
                for i, c in enumerate(e['node']['edge_sidecar_to_children']['edges']):
                    down_img(c['node'], dest, sess, e['node']['shortcode'], '-{:02d}'.format(i))
            else:
                down_img(e['node'], dest, sess)
        variables['after'] = res['page_info']['end_cursor']
        if not variables['after']:
            break