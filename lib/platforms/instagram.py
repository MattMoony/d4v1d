"""Contains methods for crawling Instagram (https://www.instagram.com/)."""

import random
import requests as req
from lib.models.user import User
from lib.platforms import Platform
from lib.models.picture import Picture
from lib.errors import UnknownUserException
from typing import *

class Instagram(Platform):
    """Represents the Instagram platform"""

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
        'login': 'https://i.instagram.com/api/v1/accounts/login/',
        'followers': 'https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables={}',
        'following': 'https://www.instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables={}',
        'media': 'https://www.instagram.com/graphql/query/?query_hash=e769aa130647d2354c40ea6a439bfc08&variables={}',
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
            'X-FB-HTTP-Engine': cls.params['FB_HTTP_ENGINE'],
        }

    @classmethod
    def get_user(cls, session: req.Session, username: str, headers: Optional[Dict[str, str]] = None) -> User:
        """Gets a basic overview of an Instagram account"""
        res: object = session.get(cls.endpoints['public_info'].format(username), headers=headers).json()
        if not len(res.keys()):
            raise UnknownUserException(f'User "{username}" cannot be found on platform Instagram ... ')
        res = res['graphql']['user']
        return User(username, 'Instagram', res['is_private'], res['is_verified'], 
                    profile_pic=Picture(url=res['profile_pic_url_hd']), fullname=res['full_name'], 
                    website=res['external_url'], bio=res['biography'])
