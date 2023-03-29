"""
Defines the database schema for SQL databases.
"""

from typing import Dict

SQLSchema: Dict[str, Dict[str, str]] = {
    'users': {
        'id': 'INTEGER NOT NULL',
        'timestamp': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
        'username': 'VARCHAR(32) NOT NULL',
        'about_me': 'VARCHAR(150)',
        'followers': 'INTEGER',
        'following': 'INTEGER',
        'number_tells': 'INTEGER',
        'avatar_file_name_local': 'VARCHAR(256)',
        '.pk': [
                'id',
                'timestamp',
        ],
    },
    'tells': {
        'id': 'INTEGER NOT NULL',
        'timestamp': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
        'post_type': 'INTEGER NOT NULL',
        'answer': 'VARCHAR(150) NOT NULL',
        'likes_count': 'INTEGER',
        'created_at': 'TIMESTAMP',
        'tell': 'VARCHAR(150) NOT NULL',
        'owner': 'INTEGER NOT NULL',
        '.pk': [
            'id',
            'created_at',
            'owner',
        ],
        '.fk': [
            (('owner',), 'users', ('id',), ),
        ],
    }
}
