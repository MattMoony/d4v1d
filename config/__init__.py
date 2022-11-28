"""
Some basic parameters important / useful to the
entire application.
"""

import os
import platform
from typing import *

"""The path to the root folder of this application"""
BASE_PATH: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

"""The prompt to be displayed to the user"""
PROMPT: str = f'<b><aaa fg="Tomato">[{os.getlogin()}@{platform.node()}</aaa> d4v1d%%<aaa fg="Tomato">]$</aaa></b> '

"""Complete commands while typing?"""
COMPLETE_WHILE_TYPING: bool = True