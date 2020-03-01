import re
import json
import uuid
import random
import requests as req

USER_AGENT_FORMAT = \
        'Instagram {app_version} Android ({android_version:d}/{android_release}; ' \
        '{dpi}; {resolution}; {brand}; {device}; {model}; {chipset}; en_US; {version_code})'

USER_AGENT_EXPRESSION = \
        r'Instagram\s(?P<app_version>[^\s]+)\sAndroid\s\((?P<android_version>[0-9]+)/(?P<android_release>[0-9\.]+);\s' \
        r'(?P<dpi>\d+dpi);\s(?P<resolution>\d+x\d+);\s(?P<manufacturer>[^;]+);\s(?P<device>[^;]+);\s' \
        r'(?P<model>[^;]+);\s(?P<chipset>[^;]+);\s[a-z]+_[A-Z]+;\s(?P<version_code>\d+)'

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

USER_AGENT = USER_AGENT_FORMAT.format(**{
        'app_version': APP_VERSION,
        'android_version': ANDROID_VERSION,
        'android_release': ANDROID_RELEASE,
        'brand': PHONE_MANUFACTURER,
        'device': PHONE_DEVICE,
        'model': PHONE_MODEL,
        'dpi': PHONE_DPI,
        'resolution': PHONE_RESOLUTION,
        'chipset': PHONE_CHIPSET,
        'version_code': VERSION_CODE})

USERNAME = 'matt_moony'
# USER_ID = '7383720597'

def default_headers():
    return {
        'User-Agent': USER_AGENT,
        'Connection': 'close',
        'Accept': '*/*',
        'Accept-Language': 'en-US',
        'Accept-Encoding': 'gzip, deflate',
        'X-IG-Capabilities': IG_CAPABILITIES,
        'X-IG-Connection-Type': 'WIFI',
        'X-IG-Connection-Speed': '{0:d}kbps'.format(random.randint(1000, 5000)),
        'X-IG-App-ID': APPLICATION_ID,
        'X-IG-Bandwidth-Speed-KBPS': '-1.000',
        'X-IG-Bandwidth-TotalBytes-B': '0',
        'X-IG-Bandwidth-TotalTime-MS': '0',
        'X-FB-HTTP-Engine': FB_HTTP_ENGINE,
    }

def get_userid(uname):
    r = json.loads(req.get('https://www.instagram.com/{}?__a=1'.format(uname)).text)
    return r['graphql']['user']['id']

def main():
    res = req.get('https://i.instagram.com/api/v1/friendships/{0}/following/'.format(get_userid(USERNAME)), headers={
                        **default_headers(), 
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},
                    cookies={
                        'csrftoken': '7stDycqfq4w6TkhuD4y5Y3JoaLMe1Xez',
                        'ds_user_id': '1417718197',
                        'ig_cb': '1',
                        'ig_did': '4ED5A9E4-28E9-40ED-9AB0-39A7C177D907',
                        'mid': 'XlwFEgALAAEEfzkSmFRkMD15D9TD',
                        'rur': 'PRN',
                        'sessionid': '1417718197%3AeYuEYhmZJE7zFP%3A16',
                        'shbid': '15399',
                        'shbts': '1583088955.016041',
                        'urlgen': '"{\"77.119.128.20\": 25255}:1j8Tv7:E9sjOa9RMfjK_WCvBjxpd6XDPEQ"',
                    })
    with open("out.html", "w") as f:
        f.write(res.text)
    following = json.loads(res.text)['users']
    print('Following {} accounts ... '.format(len(following)))
    with open('following.json', 'w') as f:
        json.dump(following, f)

if __name__ == '__main__':
    main()