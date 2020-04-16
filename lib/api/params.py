import os.path
from typing import Dict

BASE_PATH: str = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', '..'))
TMP_PATH: str = os.path.abspath(os.path.join(BASE_PATH, 'tmp'))
SRV_PATH: str = os.path.abspath(os.path.join(BASE_PATH, 'server'))

IG_SIG_KEY: str = '19ce5f445dbfd9d29c59dc2a78c616a7fc090a8e018b9267bc4240a30244c53b'
IG_CAPABILITIES: str = '3brTvw=='
SIG_KEY_VERSION: str = '4'
APPLICATION_ID: str = '567067343352427'
FB_HTTP_ENGINE: str = 'Liger'

USER_AGENT: Dict[str, str] = {
    'APP_VERSION': '76.0.0.15.395',
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

PPIC_NAME: str = 'pp{}.jpg'

PAUSE_TIME: int = 5
BOT_TIMEOUT: int = 86400