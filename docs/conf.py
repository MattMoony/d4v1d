# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
import datetime
from typing import *

BPATH: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path = [ BPATH, os.path.join(BPATH, 'd4v1d') ] + sys.path

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project: str = 'd4v1d'
author: str = 'm4ttm00ny'
copyright: str = f'{datetime.datetime.now().year}, {author}'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions: List[str] = [ 
    'sphinx.ext.autodoc', 
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'myst_parser',
]

source_suffix: Dict[str, str] = { 
    '.rst': 'restructuredtext', 
    '.md': 'markdown', 
}

templates_path: List[str] = [ '_templates', ]
exclude_patterns: List[str] = [ '_build', 'Thumbs.db', '.DS_Store', ]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme: List[str] = 'pydata_sphinx_theme'
html_static_path: List[str] = [ '_static', ]
html_title: str = 'd4v1d'
html_logo: str = '_static/logo.png'
html_favicon: str = '_static/favicon.ico'

html_theme_options:  Dict[str, Any] = {
    'logo': {
        'text': 'd4v1d',
    },
    'github_url': 'https://github.com/MattMoony/d4v1d',
    'navbar_align': 'left',
    'navbar_end': [
        'navbar-icon-links',
        'search-field',
    ],
    'icon_links': [
        {
            'name': 'PyPI',
            'url': 'https://pypi.org/project/d4v1d/',
            'icon': 'fab fa-python',
        },
    ],
}

html_context: Dict[str, Any] = {
    'github_user': 'MattMoony',
    'github_repo': 'd4v1d',
    'github_version': 'master',
    'doc_path': 'docs',
}
