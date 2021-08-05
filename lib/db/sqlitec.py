import os, csv, pathlib
import sqlite3
import lib.params
from lib.models.user import User
from typing import *

class SQLiteController(object):
    """DB Controller for SQLite databases"""

    """The DDL required for database setup"""
    __setup: List[str] = [
        '''
            CREATE TABLE IF NOT EXISTS platforms (
                pid         INTEGER PRIMARY KEY,
                name        TEXT NOT NULL UNIQUE,
                link        TEXT NOT NULL
            )
        ''',
        '''
            CREATE TABLE IF NOT EXISTS users (
                username    TEXT,
                pid         INTEGER,
                FOREIGN KEY (pid) REFERENCES platform(pid),
                PRIMARY KEY (username, pid)
            )
        ''',
        '''
            CREATE TABLE IF NOT EXISTS overviews (
                username    TEXT,
                pid         INTEGER,
                timestamp   INTEGER DEFAULT CURRENT_TIMESTAMP,
                private     BOOLEAN NOT NULL,
                verified    BOOLEAN NOT NULL,
                profile_pic TEXT,
                fullname    TEXT,
                website     TEXT,
                bio         TEXT,
                FOREIGN KEY (username) REFERENCES users(username),
                FOREIGN KEY (pid) REFERENCES users(pid),
                PRIMARY KEY (username, pid, timestamp)
            )
        ''',
    ]

    def __init__(self, dbname: str = os.path.join(lib.params.DATA_PATH, 'data.db')):
        self.dbname: str = dbname
        self.con: sqlite3.Connection = sqlite3.connect(self.dbname)

    def setup(self) -> None:
        """Creates all necessary tables, etc."""
        c: sqlite3.Cursor = self.con.cursor()
        for l in SQLiteController.__setup:
            c.execute(l)
        with open(os.path.join(lib.params.BASE_PATH, 'lib', 'db', 'platforms.csv'), 'r') as f:
            for p in csv.DictReader(f):
                try:
                    c.execute('INSERT INTO platforms (name, link) VALUES (?, ?)', (p['name'], p['link'],))
                except sqlite3.IntegrityError:
                    pass
        self.con.commit()

    def get_platform(self, pid: Optional[int] = None, name: Optional[str] = None) -> Tuple[int, str, str]:
        """Gets the id, name and link of a platform"""
        c: sqlite3.Cursor = self.con.cursor()
        if pid:
            c.execute('SELECT pid, name, link FROM platforms WHERE pid = ?', (pid,))
        else:
            c.execute('SELECT pid, name, link FROM platforms WHERE LOWER(name) = LOWER(?)', (name,))
        platform: Tuple[int, str, str] = c.fetchone()
        return platform

    def user_exists(self, pid: int, username: str) -> bool:
        """Checks, if a user on a given platform has been recorded"""
        c: sqlite3.Cursor = self.con.cursor()
        c.execute('SELECT username, pid FROM users WHERE username = ? AND pid = ?', (username, pid,))
        res: Optional[Tuple[str, int]] = c.fetchone()
        return res != None

    def store_user(self, user: User) -> None:
        """Stores a social-media user in the SQLite db"""
        pic_path: str = os.path.join(lib.params.DATA_PATH, user.username, user.platform, f'profile.{user.profile_pic.ext()}')
        pathlib.Path(os.path.dirname(pic_path)).mkdir(parents=True, exist_ok=True)
        if user.profile_pic:
            user.profile_pic.write(pic_path)
        c: sqlite3.Cursor = self.con.cursor()
        platform: Tuple[int, str, str] = self.get_platform(name=user.platform)
        if not self.user_exists(platform[0], user.username):
            c.execute('INSERT INTO users (username, pid) VALUES (?, ?)', (user.username, platform[0]))
        c.execute('''INSERT INTO overviews (username, pid, private, verified, profile_pic, fullname, website, bio)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                  (user.username, platform[0], user.private, user.verified, 
                   pic_path if user.profile_pic else '', user.fullname or '', user.website or '', user.bio or ''))
        self.con.commit()
