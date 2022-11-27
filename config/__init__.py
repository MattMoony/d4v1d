"""
Some basic parameters important / useful to the
entire application.
"""

import os
from prompt_toolkit.formatted_text.html import HTML

"""The path to the root folder of this application"""
BASE_PATH: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

"""The prompt to be displayed to the user"""
PROMPT: HTML = HTML(f'<b><aaa fg="Tomato">[{os.getlogin()}@{os.uname().nodename}</aaa> d4v1d<aaa fg="Tomato">]$</aaa></b> ')

"""Complete commands while typing?"""
COMPLETE_WHILE_TYPING: bool = True