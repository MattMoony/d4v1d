"""
Defines the database schema for SQL databases.
"""

from typing import Dict

SQLSchema: Dict[str, Dict[str, str]] = {
    'users': {
        'id': 'INTEGER NOT NULL',
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
    'posts': {
        'id': 'INTEGER NOT NULL',
        'timestamp': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
        'shortcode': 'VARCHAR(16) NOT NULL',
        'caption': 'VARCHAR(2304) NOT NULL',
        'width': 'INTEGER NOT NULL',
        'height': 'INTEGER NOT NULL',
        'is_video': 'BOOLEAN NOT NULL',
        'comments_disabled': 'BOOLEAN NOT NULL',
        'taken_at_timestamp': 'TIMESTAMP',
        'likes': 'INTEGER NOT NULL',
        'owner': 'INTEGER NOT NULL',
        'location': 'INTEGER',
        '.pk': [
            'id',
            'timestamp',
            'owner',
        ],
        '.fk': [
            ( ('owner',), 'users', ('id',), ),
            ( ('location',), 'locations', ('id',), ),
        ],
    },
    'images': {
        'id': 'INTEGER NOT NULL',
        'timestamp': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
        'post': 'INTEGER NOT NULL',
        'path_local': 'VARCHAR(256) NOT NULL',
        'width': 'INTEGER NOT NULL',
        'height': 'INTEGER NOT NULL',
        'is_video': 'BOOLEAN NOT NULL',
        '.pk': [
            'id',
            'timestamp',
            'post',
        ],
        '.fk': [
            ( ('post',), 'posts', ('id',), ),
        ],
    },
    'locations': {
        'id': 'INTEGER NOT NULL',
        'has_public_page': 'BOOLEAN NOT NULL',
        'name': 'VARCHAR(128) NOT NULL',
        'slug': 'VARCHAR(128) NOT NULL',
        '.pk': [
            'id',
        ],
    },
}
