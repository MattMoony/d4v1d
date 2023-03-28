"""
Database implementation for an SQLite database.
"""

import os
import re
import sqlite3
import uuid
from datetime import datetime
from typing import List, Optional, Tuple

from d4v1d import config
from d4v1d.log import log
from d4v1d.platforms.instagram.db.database import Database
from d4v1d.platforms.instagram.db.models import InstagramUser
from d4v1d.platforms.instagram.db.models.location import InstagramLocation
from d4v1d.platforms.instagram.db.models.media import InstagramMedia
from d4v1d.platforms.instagram.db.models.post import InstagramPost
from d4v1d.platforms.instagram.db.schema.sql import SQLSchema
from d4v1d.platforms.platform.info import Info
from d4v1d.platforms.platform.mediatype import MediaType


class SQLiteDatabase(Database):
    """
    SQLite database for Instagram information
    """

    def __init__(self, path: Optional[str] = None):
        """
        Creates a new SQLiteDatabase object

        Args:
            path (Optional[str], optional): The path to the database file.
                If None, the database will be stored in the data directory
                used by all platforms as specified in the config file.
        """
        super().__init__()
        # we can assume that the data directory for instagram exists
        # at this point, because it is created in the init function
        # of this platform module
        self.path: str = path or os.path.join(config.PCONFIG._instagram.ddir, 'instagram.db')
        # check if the db exists ...
        if os.path.isfile(self.path):
            # establish a connection to the database
            self.con: sqlite3.Connection = sqlite3.connect(self.path)
            # check the database for any schema errors
            if not self.__health_check():
                # close the connection to the old db
                self.con.close()
                # generate a new, unique backup id & move the file
                bak: str = str(uuid.uuid4())
                while os.path.exists(os.path.join(config.PCONFIG._instagram.ddir, f'{bak}.db')):
                    bak = str(uuid.uuid4())
                log.warning('Database is not in a valid state - backing up to [bold]%s/%s.db[/bold] and creating a new database', config.PCONFIG._instagram.ddir, bak)
                os.rename(os.path.join(config.PCONFIG._instagram.ddir, 'instagram.db'), os.path.join(config.PCONFIG._instagram.ddir, f'{bak}.db'))
                # connect to the new db & create everything
                self.con = sqlite3.connect(self.path)
                self.__setup_database()
        else:
            # connect to the new db & create everything
            self.con = sqlite3.connect(self.path)
            self.__setup_database()

    def __del__(self) -> None:
        """
        Do some cleanup, once the platform is unloaded
        in the d4v1d core
        """
        log.debug('Cleaning up Instagram database ... ')
        self.con.close()

    def __health_check(self) -> bool:
        """
        Checks if the database is in a valid state - only confirms the
        presence of all tables, however - if this method returns False,
        the database should be deleted / backed up and created again.

        Returns:
            bool: True if the database is valid, False otherwise
        """
        try:
            for table in SQLSchema:
                # check if the table exists
                c: sqlite3.Cursor = self.con.cursor()
                c.execute('SELECT name FROM sqlite_master WHERE type=? AND name=?', ('table', table))
                if c.fetchone() is None:
                    return False
            return True
        except Exception:  # pylint: disable=broad-exception-caught
            return False

    def __setup_database(self) -> None:
        """
        Creates the database tables and sets up the database
        """
        # iterate over defined tables and their specifications
        for table, spec in SQLSchema.items():
            # TODO: should improve / change this, it's
            # not cool to do it this way, but... it's
            # semi-safe for now - i'm well aware that
            # this is not the best code ... :P
            __safe: str = r'[\w\(\)\._ ]+'
            def __burn_everything_to_the_ground(s: str) -> None:
                msg: str = f'Invalid symbol in SQLite DB creation: {s} - refusing to continue'
                log.critical(msg)
                log.critical('Crashing everything, since this shouldn\'t happen unless someone messed with the schema ([bold][red]danger of SQLi !!![/red][/bold])')
                log.critical('Compare your schema ("%s") with the original', os.path.join(os.path.dirname(__file__), "schema", "sql.py"))
                raise ValueError(msg)
            if not re.match(__safe, table):
                # crash everything - since this should DEFINITELY
                # not happen unless someone messed with the schema
                __burn_everything_to_the_ground(table)
            # TODO: clean this up a little bit?! I split up 
            # the if into multiple lines to make it at least 
            # a little more readable
            if any(
                not (
                    # check if the key is safe
                    re.match(__safe, k)
                    # check if the value is safe
                    and (
                        # if the key's a column name, check
                        # the definition for safety - regular string check
                        re.match(__safe, v)
                        if isinstance(v, str)
                        else all(
                            # if the key is '.pk' - i.e. the list of primary 
                            # keys, check all key names
                            re.match(__safe, _)
                            if isinstance(_, str)
                            else all(
                                # check the names of the referenced tables
                                # in case of the key being '.fk' - foreign keys
                                re.match(__safe, __)
                                if isinstance(__, str)
                                else all(
                                    # check the names of the referenced columns
                                    # in case of the key being '.fk' - foreign keys
                                    re.match(__safe, ___)
                                    for ___ in __
                                )
                                for __ in _
                            )
                            for _ in v)
                        )
                    )
                for k, v in spec.items()
            ):
                __burn_everything_to_the_ground('')
            # create the table
            c: sqlite3.Cursor = self.con.cursor()
            qry: str = f'''CREATE TABLE {table} (
                {", ".join([f"{k} {v}" for k, v in spec.items() if k[0] != "."])},
                PRIMARY KEY ({", ".join(spec[".pk"])}){f""",
                {', '.join(f'FOREIGN KEY ({", ".join(cols)}) REFERENCES {tbl}({", ".join(fks)})' for cols, tbl, fks in spec['.fk'])}
                """ if ".fk" in spec else ""})'''
            log.debug('Creating table [bold]%s[/bold] using ... ', table)
            log.debug(qry)
            c.execute(qry)
        self.con.commit()

    def store_user(self, user: InstagramUser) -> None:
        """
        Stores a user in the database

        Args:
            user (User): The user to store
        """
        c: sqlite3.Cursor = self.con.cursor()
        c.execute('''INSERT INTO users (
            id, fbid, username, full_name, bio, followers,
            following, profile_pic_local, private, number_posts,
            category_name, pronouns
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )''', user.dumpt())
        self.con.commit()

    def store_posts(self, posts: List[Info[InstagramPost]]) -> None:
        """
        Stores a list of posts in the database

        Args:
            posts (List[Info[Post]]): The posts to store
        """
        c: sqlite3.Cursor = self.con.cursor()
        c.executemany('''INSERT INTO posts (
            timestamp, id, shortcode, caption, width, height,
            is_video, comments_disabled, taken_at_timestamp,
            likes, owner, location
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )''', [(post.date.isoformat(), *post.value.dumpt(),) for post in posts])
        self.con.commit()
        # store other, post-associated data ...
        for p in posts:
            if p.value.location:
                self.store_location(p.value.location)
            self.store_media(p.value.media, timestamp=p.date)

    def update_posts(self, posts: List[Info[InstagramPost]]) -> None:
        """
        Updates a list of posts in the database

        Args:
            posts (List[Info[Post]]): The posts to update
        """
        c: sqlite3.Cursor = self.con.cursor()
        c.executemany('''UPDATE posts SET
            shortcode = ?, caption = ?, width = ?, height = ?,
            is_video = ?, comments_disabled = ?, taken_at_timestamp = ?,
            likes = ?, location = ?
        WHERE id = ?
              AND timestamp = ?
              AND owner = ?''', [(
                    post.value.short_code,
                    post.value.caption,
                    *post.value.dimensions,
                    post.value.is_video,
                    post.value.comments_disabled,
                    post.value.taken_at.isoformat(),
                    post.value.likes,
                    post.value.location.id if post.value.location else None,
                    post.value.id,
                    post.date.isoformat(),
                    post.value.owner.id,
                    ) for post in posts])
        self.con.commit()
        # update other, post-associated data ...
        for p in posts:
            self.update_media(p.value.media, timestamp=p.date)

    def store_media(self, media: List[Info[InstagramMedia]], timestamp: Optional[datetime] = None) -> None:
        """
        Stores a list of media in the database.

        Args:
            media (List[Info[InstagramMedia]]): The media to store.
            timestamp (Optional[datetime]): The timestamp of the post the media belongs to.
        """
        if any(not isinstance(m, Info) for m in media) and timestamp is None:
            raise ValueError('If media is not a list of Info objects, timestamp must be specified')
        c: sqlite3.Cursor = self.con.cursor()
        c.executemany('''INSERT INTO media (
                            timestamp, id, post, type, url, path, width, height
                         ) VALUES (
                            ?, ?, ?, ?, ?, ?, ?, ?
                         )''', [(m.date.isoformat() if isinstance(m, Info) else timestamp.isoformat(), *(m.value.dumpt() if isinstance(m, Info) else m.dumpt()),) for m in media])
        self.con.commit()

    def update_media(self, media: List[Info[InstagramMedia]], timestamp: Optional[datetime] = None) -> None:
        """
        Updates a list of media in the database.

        Args:
            media (List[Info[InstagramMedia]]): The media to update.
            timestamp (Optional[datetime]): The timestamp of the post the media belongs to.
        """
        if any(not isinstance(m, Info) for m in media) and timestamp is None:
            raise ValueError('If media is not a list of Info objects, timestamp must be specified')
        c: sqlite3.Cursor = self.con.cursor()
        c.executemany('''UPDATE media SET
                            type = ?, url = ?, path = ?, width = ?, height = ?
                         WHERE id = ?
                               AND timestamp = ?
                               AND post = ?''', [(
                                m.value.type.value,
                                m.value.url,
                                m.value.path,
                                *m.value.dimensions,
                                m.value.id,
                                m.date.isoformat(),
                                m.value.post.id,
                         ) if isinstance(m, Info) else (
                                m.type.value,
                                m.url,
                                m.path,
                                *m.dimensions,
                                m.id,
                                timestamp.isoformat(),
                                m.post.id,
                         ) for m in media])
        self.con.commit()

    def store_location(self, location: InstagramLocation) -> None:
        """
        Stores a location in the database

        Args:
            location (Location): The location to store
        """
        if self.get_location(location.id):
            # already exists, ignore ...
            return
        c: sqlite3.Cursor = self.con.cursor()
        c.execute('''INSERT INTO locations (
            id, has_public_page, name, slug
        ) VALUES (
            ?, ?, ?, ?
        )''', location.dumpt())
        self.con.commit()

    def get_user(self, username: Optional[str] = None, id: Optional[int] = None) -> Optional[Info[InstagramUser]]:
        """
        Gets a user from the database.

        Args:
            username (Optional[str]): The username of the user.
            id (Optional[int]): The id of the user.

        Returns:
            Optional[Info[User]]: The user if it exists, None otherwise.
        """
        if username is None and id is None:
            raise ValueError('Either username or id must be specified')
        c: sqlite3.Cursor = self.con.cursor()
        c.execute(f'''SELECT
                        STRFTIME('%s', timestamp), id, fbid, username, full_name, bio, followers,
                        following, profile_pic_local, private, number_posts,
                        category_name, pronouns
                     FROM users 
                     WHERE {f'username = ?' if username is not None else 'id = ?'}
                     ORDER BY timestamp DESC
                     LIMIT 1''', (username if username is not None else id,))
        row: Optional[Tuple] = c.fetchone()
        if row is None:
            return None
        return Info(InstagramUser(*row[1:]), datetime.fromtimestamp(int(row[0])))

    def get_users(self) -> List[Info[InstagramUser]]:
        """
        Get a list of all users in the DB.

        Returns:
            List[Info[User]]: List of all user infos in the db (normally ordered by username).
        """
        c: sqlite3.Cursor = self.con.cursor()
        c.execute('''SELECT
                        STRFTIME('%s', timestamp), id, fbid, username, full_name, bio, followers,
                        following, profile_pic_local, private, number_posts,
                        category_name, pronouns
                     FROM users u
                     WHERE timestamp = (SELECT MAX(timestamp)
                                        FROM users
                                        WHERE id = u.id)
                     ORDER BY username;
                  ''')
        return [ Info(InstagramUser(*row[1:]), datetime.fromtimestamp(int(row[0]))) for row in c.fetchall() ]

    def get_posts(self, user: InstagramUser, _from: datetime, _to: datetime) -> List[Info[InstagramPost]]:
        """
        Gets a list of posts from a user

        Args:
            user (User): The user to get the posts from
            _from (datetime.datetime): The start of the time range
            _to (datetime.datetime): The end of the time range

        Returns:
            List[Info[Post]]: The posts
        """
        c: sqlite3.Cursor = self.con.cursor()
        c.execute(f'''SELECT
                        timestamp, id, shortcode, caption, width, height,
                        is_video, comments_disabled, taken_at_timestamp,
                        likes, owner, location
                     FROM posts p
                     WHERE owner=?
                           {f'AND timestamp >= ? AND ' if _from is not None else ''}
                           {f'AND timestamp <= ?' if _to is not None else ''}
                           AND timestamp = (SELECT MAX(timestamp)
                                            FROM posts
                                            WHERE id = p.id
                                                  AND owner = p.owner)
                     ORDER BY taken_at_timestamp DESC''', 
                     (user.id,) + ((_from.isoformat(),) if _from else ()) + ((_to.isoformat(),) if _to else ()))
        posts: List[Info[InstagramPost]] = [Info(InstagramPost(
                                                    *row[1:4], 
                                                    tuple(row[4:6]), 
                                                    *row[6:8], 
                                                    datetime.fromisoformat(row[8]), 
                                                    *row[9:10],
                                                    owner = self.get_user(id=row[10]).value,
                                                    location = self.get_location(row[11]) if row[11] is not None else None
                                            ), datetime.fromisoformat(row[0])) for row in c.fetchall()]
        for p in posts:
            p.value.media = [ _.value for _ in self.get_media(p) ]
        return posts
    
    def get_media(self, post: Info[InstagramPost]) -> List[Info[InstagramMedia]]:
        """
        Gets a list of media from a post

        Args:
            post (Info[InstagramPost]): The post to get the media from

        Returns:
            List[Info[InstagramMedia]]: The media
        """
        c: sqlite3.Cursor = self.con.cursor()
        c.execute('''SELECT
                        timestamp, id, type, url, width, height, path
                     FROM media
                     WHERE post = ?
                           AND timestamp = ?
                     ORDER BY timestamp DESC''', (post.value.id, post.date.isoformat()))
        media: List[Info[InstagramMedia]] = [Info(InstagramMedia(row[1], MediaType(row[2]), row[3], tuple(row[4:6]), *row[6:]), datetime.fromisoformat(row[0])) for row in c.fetchall()]
        for m in media:
            m.value.post = post.value
        return media

    def get_location(self, id: int) -> Optional[InstagramLocation]:
        """
        Gets a location from the database

        Args:
            id (int): The id of the location

        Returns:
            Optional[InstagramLocation]: The location if it exists, None otherwise.
        """
        c: sqlite3.Cursor = self.con.cursor()
        c.execute('''SELECT
                        id, has_public_page, name, slug
                     FROM locations
                     WHERE id = ?''', (id,))
        row: Optional[Tuple] = c.fetchone()
        if row is None:
            return None
        return InstagramLocation(*row)
