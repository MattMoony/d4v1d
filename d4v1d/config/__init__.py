"""
Some basic parameters important / useful to the
entire application.
"""

import json
import os
import platform
from typing import Dict

import pkg_resources

from d4v1d.config.platforms import PlatformsConfig

BASE_PATH: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
"""The path to the root folder of this application"""

PROMPT: str = f'<b><aaa fg="Tomato">[{os.getlogin()}@{platform.node()}</aaa> d4v1d%%<aaa fg="Tomato">]$</aaa></b> '
PROMPT: str = f'<b>{platform.node()}/{os.getlogin()} <u>d4v1d<aaa fg="Tomato">%%</aaa></u> <aaa fg="Grey"># </aaa></b>'
"""The prompt to be displayed to the user"""

COMPLETE_WHILE_TYPING: bool = True
"""Complete commands while typing?"""

PLATFORMS: Dict[str, str] = {}
"""Contains various config options for platforms"""

LOG_NAME: str = 'd4v1d'
"""The name of the logger"""

LOG_FORMAT: str = '%(message)s'
"""The format for error/warning log messages"""

LOG_LEVEL: str = 'WARNING'
"""The default log level for the logger"""

LOG_DATEFMT: str = '[%X]'
"""The date format for log messages"""

PCONFIG: PlatformsConfig
"""Contains various config options for platforms"""

with open(pkg_resources.resource_filename('d4v1d', 'data/platforms.conf.json'), 'r', encoding='utf8') as f:
    PCONFIG = PlatformsConfig.loadj(json.load(f))
