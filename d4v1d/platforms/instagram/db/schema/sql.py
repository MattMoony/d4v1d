"""
Defines the database schema for SQL databases.
"""

from typing import *

SQLSchema: Dict[str, Dict[str, str]] = {
    'users': {
        'id': 'INTEGER',
        'timestamp': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
        'fbid': 'INTEGER',
        'username': 'VARCHAR(32) NOT NULL',
        'full_name': 'VARCHAR(64)',
        'bio': 'VARCHAR(150)',
        'followers': 'INTEGER',
        'following': 'INTEGER',
        'profile_pic_local': 'VARCHAR(256)',
        'private': 'BOOLEAN',
        'number_posts': 'INTEGER',
        'category_name': 'VARCHAR(32)',
        'pronouns': 'VARCHAR(16)',
        '.pk': [
            'id',
            'timestamp',
        ],
    },
    'links': {
        'id': 'INTEGER AUTO_INCREMENT',
        'url': 'VARCHAR(2048) NOT NULL',
        '.pk': [
            'id',
        ],
    },
    'user_links': {
        'user': 'INTEGER NOT NULL',
        'link': 'INTEGER NOT NULL',
        'timestamp': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
        '.pk': [
            'user',
            'link',
            'timestamp',
        ],
    },
    'user_references': {
        'referrer': 'INTEGER NOT NULL',
        'referring': 'INTEGER NOT NULL',
        'timestamp': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
        'context': 'VARCHAR(16)',
        '.pk': [
            'referrer',
            'referring',
            'timestamp',
        ],
    },
}
