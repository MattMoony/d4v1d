# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

BPATH: str = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(BPATH, 'README.md'), 'r', encoding='utf-8') as f:
    LONG_DESCRIPTION: str = f.read()

def version() -> str:
    from d4v1d.__version__ import version
    return version

setup(
    name='d4v1d',
    version=version(),
    author='m4ttm00ny',
    author_email='m4ttm00ny@gmail.com',
    description=(
        'Social-Media OSINT tool - gather info on users across multiple platforms; easily extensible by design. 📷',
    ),
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/MattMoony/d4v1d',
    project_urls={
        'Homepage': 'https://github.com/MattMoony/d4v1d',
        'Documentation': 'https://m4ttm00ny.xyz/d4v1d',
        'Source': 'https://github.com/MattMoony/d4v1d',
        'Tracker': 'https://github.com/MattMoony/d4v1d/issues',
    },
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: Security',
    ],
    entry_points={
        'console_scripts': [
            'd4v1d = d4v1d.cli:main',
        ],
    },
    install_requires=[
        'colorama',
        'prompt-toolkit',
        'requests',
        'rich',
    ],
)