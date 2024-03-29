"""Contains methods for crawling Instagram (https://www.instagram.com/)."""

import random, datetime, re, json, math
import requests as req
from urllib.parse import quote
from lib.misc import print_wrn
from lib.models import User
from lib.models.media import Media
from lib.platforms import Platform
from lib.errors import UnknownUserError
from typing import *

class Instagram(Platform):
    """Represents the Instagram platform"""

    name: str = 'Instagram'
    link: str = 'https://instagram.com/'

    """Defines some social-media platform specific parameters"""
    params: Dict[str, str] = {
        'IG_SIG_KEY': '19ce5f445dbfd9d29c59dc2a78c616a7fc090a8e018b9267bc4240a30244c53b',
        'IG_CAPABILITIES': '3brTvw==',
        'SIG_KEY_VERSION': '4',
        'APP_VERSION': '76.0.0.15.395',
        'APPLICATION_ID': '567067343352427',
        'FB_HTTP_ENGINE': 'Liger',

        'ANDROID_VERSION': 24,
        'ANDROID_RELEASE': '7.0',
        'PHONE_MANUFACTURER': 'samsung',
        'PHONE_DEVICE': 'SM-G930F',
        'PHONE_MODEL': 'herolte',
        'PHONE_DPI': '640dpi',
        'PHONE_RESOLUTION': '1440x2560',
        'PHONE_CHIPSET': 'samsungexynos8890',
        'VERSION_CODE': '138226743',
    }

    """Contains endpoints required for all interactions with the platform"""
    endpoints: Dict[str, str] = {
        'login': 'https://www.instagram.com/accounts/login/',
        'post_login': 'https://www.instagram.com/accounts/login/ajax/',
        'followers': 'https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables={}',
        'following': 'https://www.instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables={}',
        'media': 'https://www.instagram.com/graphql/query/?query_hash=e769aa130647d2354c40ea6a439bfc08&variables={}',
        'post': 'https://www.instagram.com/graphql/query/?query_hash=2efa04f61586458cef44441f474eee7c&variables={"shortcode":"{shortcode}","child_comment_count":3,"fetch_comment_count":40,"parent_comment_count":24,"has_threaded_comments":true}',
        'comments': 'https://www.instagram.com/graphql/query/?query_hash=bc3296d1ce80a24b1b6e40b1e72903f5&variables={"shortcode":"{shortcode}","first":{first},"after":"{after}"}',
        'comment_replies': 'https://www.instagram.com/graphql/query/?query_hash=1ee91c32fc020d44158a3192eda98247&variables={"comment_id":"{id}","first":{first},"after":"{after}"}',
        'info': 'https://i.instagram.com/api/v1/users/{}/info/',
        'public_info': 'https://www.instagram.com/{}/?__a=1',
    }

    @classmethod
    def get_user_agent(cls) -> str:
        """Helper function to generate the default user agent"""
        return 'Instagram {} Android ({}/{}; {}; {}; {}; {}; {}; {}; en_US; {})'\
                .format(cls.params['APP_VERSION'], cls.params['ANDROID_VERSION'], cls.params['ANDROID_RELEASE'],
                        cls.params['PHONE_MANUFACTURER'], cls.params['PHONE_DEVICE'], cls.params['PHONE_MODEL'],
                        cls.params['PHONE_DPI'], cls.params['PHONE_RESOLUTION'], cls.params['PHONE_CHIPSET'], 
                        cls.params['VERSION_CODE'])
        # return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.3'

    @classmethod
    def get_headers(cls) -> Dict[str, str]:
        """Returns the standard headers for Instagram"""
        return {
            'User-Agent': Instagram.get_user_agent(),
            'Connection': 'close',
            'Accept': '*/*',
            'Accept-Language': 'en-US',
            'Accept-Encoding': 'gzip, deflate',
            'X-IG-Capabilities': cls.params['IG_CAPABILITIES'],
            'X-IG-Connection-Type': 'WIFI',
            'X-IG-Connection-Speed': '{0:d}kbps'.format(random.randint(1000, 5000)),
            'X-IG-App-ID': cls.params['APPLICATION_ID'],
            'X-IG-Bandwidth-Speed-KBPS': '-1.000',
            'X-IG-Bandwidth-TotalBytes-B': '0',
            'X-IG-Bandwidth-TotalTime-MS': '0',
            'X-IG-Origin-Region': 'ldc',
            'X-IG-Push-State': 'c2',
            'X-FB-HTTP-Engine': cls.params['FB_HTTP_ENGINE'],
        }

    @classmethod
    def login(cls, session: req.Session, username: str, password: str, headers: Optional[Dict[str, str]] = None) -> bool:
        """Logs into the Instagram platform using the given credentials"""
        csrf: str = re.findall(r'csrf_token\":\"(.*?)\"', session.get(cls.endpoints['login'], headers=headers).text)[0]
        res: Dict[str, Any] = session.post(cls.endpoints['post_login'], data={
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(datetime.datetime.now().timestamp())}:{password}',
            'queryParams': {},
            'optIntoOneTap': 'false',
        }, headers={ **headers, 'X-CSRFToken': csrf, }).json()
        return res['authenticated']

    @classmethod
    def get_user(cls, session: req.Session, username: str, headers: Optional[Dict[str, str]] = None) -> User:
        """Gets a basic overview of an Instagram account"""
        res: Dict[str, Any] = session.get(cls.endpoints['public_info'].format(username), headers=headers).json()
        if not len(res.keys()):
            raise UnknownUserError(f'User "{username}" cannot be found on platform Instagram ... ')
        res = res['graphql']['user']
        return User(username, 'Instagram', res['is_private'], res['is_verified'], 
                    user_id=int(res['id']), profile_pic=Media(url=res['profile_pic_url_hd']), 
                    fullname=res['full_name'], website=res['external_url'], bio=res['biography'])

    @classmethod
    def get_media(cls, session: req.Session, user_id: int, after: Optional[str] = None, headers: Optional[Dict[str, str]] = None) -> Tuple[List[Media], str]:
        """Downloads all media of an Instagram account"""
        variables: Dict[str, Any] = {
            'id': user_id,
            'first': 50,
            'after': after,
        }
        res: Dict[str, Any] = session.get(cls.endpoints['media'].format(quote(json.dumps(variables))), headers=headers)
        with open('tmp/out.html', 'wb') as f:
            f.write(res.content)
        res = res.json()
        if res['status'] != 'ok':
            return ([], None)
        res = res['data']['user']['edge_owner_to_timeline_media']
        if len(res['edges']) == 0:
            print_wrn(f'Instagram account #{user_id}', 'Couldn\'t find any media... perhaps private?')
            return ([], None)
        ret: List[Media] = []
        for e in res['edges']:
            e = e['node']
            # basename: str = f'{datetime.datetime.fromtimestamp(e["taken_at_timestamp"]).isoformat()}-{e["shortcode"]}'
            basename: str = e['shortcode']
            caption: Optional[str] = e['edge_media_to_caption']['edges'][0]['node']['text'] if e['edge_media_to_caption']['edges'] else None
            tagged: List[User] = [User(u['node']['user']['username'], 'Instagram', None, u['node']['user']['is_verified'], user_id=u['node']['user']['id']) for u in e['edge_media_to_tagged_user']['edges']]
            likes: int = e['edge_media_preview_like']['count']
            if 'edge_sidecar_to_children' in e.keys():
                zeros: int = math.floor(math.log10(len(e['edge_sidecar_to_children']['edges'])))+1
                for i, c in enumerate(e['edge_sidecar_to_children']['edges']):
                    c = c['node']
                    ret.append(Media(name=basename+'-'+str(i).rjust(zeros, '0'), 
                                     caption=caption, tagged=tagged, likes=likes,
                                     url=c['video_url'] if c['is_video'] else c['display_url']))
            else:
                ret.append(Media(name=basename,
                                 caption=caption, tagged=tagged, likes=likes,
                                 url=e['video_url'] if e['is_video'] else e['display_url']))
        return (ret, res['page_info']['end_cursor'])
