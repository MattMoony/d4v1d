"""
Some basic parameters important / useful to the
entire application.
"""

import os
import json
import platform
from typing import *

BASE_PATH: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
"""The path to the root folder of this application"""

PROMPT: str = f'<b><aaa fg="Tomato">[{os.getlogin()}@{platform.node()}</aaa> d4v1d%%<aaa fg="Tomato">]$</aaa></b> '
"""The prompt to be displayed to the user"""

COMPLETE_WHILE_TYPING: bool = True
"""Complete commands while typing?"""

PLATFORMS: Dict[str, str] = dict()
"""Contains various config options for platforms"""

with open(os.path.join(BASE_PATH, 'config', 'platforms.json'), 'r') as f:
    PLATFORMS = json.load(f)
    dir: str = os.getenv('D4V1D_DIR')

    if not dir and not PLATFORMS['dir']:
        PLATFORMS['dir'] = os.path.join(BASE_PATH, '_')
    if not os.path.isdir(PLATFORMS['dir']):
        os.mkdir(PLATFORMS['dir'])
    
    for k, v in PLATFORMS.items():
        v = v.replace('$D4V1D_DIR', PLATFORMS['dir'])
        if k.endswith('_dir') and not os.isdir(v):
            os.mkdir(v)