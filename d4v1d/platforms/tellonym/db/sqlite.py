"""
Database implementation for an SQLite database.
"""

import os
import re
import sqlite3
import uuid
from datetime import datetime
from typing import List, Optional

from d4v1d import config
from d4v1d.log import log
from d4v1d.platforms.tellonym.db.database import Database
from d4v1d.platforms.tellonym.db.models.user import TellonymUser
from d4v1d.platforms.tellonym.db.models.tell import TellonymTell
from d4v1d.platforms.tellonym.db.schema.sql import SQLSchema
from d4v1d.platforms.platform.info import Info


class SQLiteDatabase(Database):
    """
    SQLite database for Tellonym information
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
        # we can assume that the data directory for tellonym exists
        # at this point, because it is created in the init function
        # of this platform module
        self.path: str = path or os.path.join(
            config.PCONFIG._tellonym.ddir, 'tellonym.db')
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
                while os.path.exists(os.path.join(config.PCONFIG._tellonym.ddir, f'{bak}.db')):
                    bak = str(uuid.uuid4())
                log.warning(
                    'Database is not in a valid state - backing up to [bold]%s/%s.db[/bold] and creating a new database', config.PCONFIG._tellonym.ddir, bak)
                os.rename(os.path.join(config.PCONFIG._tellonym.ddir, 'tellonym.db'), os.path.join(
                    config.PCONFIG._tellonym.ddir, f'{bak}.db'))
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
        log.debug('Cleaning up Tellonym database ... ')
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
                c.execute(
                    'SELECT name FROM sqlite_master WHERE type=? AND name=?', ('table', table))
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
                log.critical(
                    'Crashing everything, since this shouldn\'t happen unless someone messed with the schema ([bold][red]danger of SQLi !!![/red][/bold])')
                log.critical('Compare your schema ("%s") with the original', os.path.join(
                    os.path.dirname(__file__), "schema", "sql.py"))
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

    def store_user(self, user: TellonymUser) -> None:
        """
        Stores a user in the database

        Args:
            user (User): The user to store
        """
        c: sqlite3.Cursor = self.con.cursor()
        c.execute('''INSERT INTO users (
            id, username, about_me, followers, following, avatar_file_name_local, number_tells
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?
        )''', user.dumpt())
        self.con.commit()

    def store_tells(self, tells: List[Info[TellonymTell]]) -> None:
        """
        Stores a list of tells in the database

        Args:
            tells (List[Info[Tell]]): The tells to store
        """
        if len(tells) <= 0:
            return
        c: sqlite3.Cursor = self.con.cursor()
        c.executemany('''INSERT INTO tells (
            timestamp, post_type, id, answer, likes_count, created_at, tell, owner
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?
        )''', [(tell.date.isoformat(), *tell.value.dumpt()) for tell in tells])
        self.con.commit()

    def update_tells(self, tells: List[Info[TellonymTell]]) -> None:
        """
        Updates a list of tells in the database

        Args:
            tells (List[Info[Tell]]): The tells to update
        """
        c: sqlite3.Cursor = self.con.cursor()
        c.execute('''UPDATE posts SET 
            id = ?, post_type = ?, answer = ?, likes_count = ?, created_at = ?, tell = ?, owner = ?
            WHERE id = ?''', [tell.value.dumpt() for tell in tells])
        self.con.commit()

    def get_user(self, username: Optional[str] = None, id: Optional[int] = None) -> Optional[Info[TellonymUser]]:
        """
        Gets a user from the database.

        Args:
            username (Optional[str]): The username of the user.
            id (Optional[int]): The id of the user.

        Returns:
            Optional[Info[User]]: The user if it exists, None otherwise.
        """
        if username is None and id is None:
            raise ValueError('Either usernamer or id must be specified')
        c: sqlite3.Cursor = self.con.cursor()
        c.execute(f'''SELECT
                        STRFTIME('%s', timestamp), id, username, about_me, followers, following, avatar_file_name_local, number_tells
                        FROM users
                        WHERE {f'username = ?' if username is not None else 'id = ?'}
                        ORDER BY timestamp DESC
                        LIMIT 1''', (username if username is not None else id,))
        row: Optional[tuple] = c.fetchone()
        print(row)
        u: TellonymUser = TellonymUser(*row[1:])
        print(u.id)
        if row is None:
            return None
        return Info(TellonymUser(*row[1:]), datetime.fromtimestamp(int(row[0])))

    def get_users(self) -> List[Info[TellonymUser]]:
        """
        Get a list of users stored in the DB.

        Returns:
            List[Info[User]]: List of info about users.
        """
        c: sqlite3.Cursor = self.con.cursor()
        c.execute('''SELECT
                        STRFTIME('%s', timestamp), id, username, about_me, followers, following, avatar_file_name_local, number_tells
                        FROM users u
                        WHERE timestamp = (SELECT MAX(timestamp)
                                            FROM users
                                            WHERE id = u.id
                                            )
                        ORDER BY username;
        ''')
        return [Info(TellonymUser(*row[1:]), datetime.fromtimestamp(int(row[0]))) for row in c.fetchall()]

    def get_tells(self, user: TellonymUser, _from: datetime, _to: datetime) -> List[Info[TellonymTell]]:
        """
        Gets a list of tells from a user

        Args:
            user (User): The user to get the tells from
            _from (datetime.datetime): The start of the time range
            _to (datetime.datetime): The end of the time range

        Returns:
            List[Info[Tell]]: The tells
        """
        print(f'''SELECT
                        timestamp, id, post_type, answer, likes_count, created_at, tell, owner
                    FROM tells t
                    WHERE owner = {user.id}
                    {f'AND timestamp >= ? ' if _from is not None else ''}
                    {f'AND timestamp <= ? ' if _to is not None else ''}
                    AND timestamp = (SELECT MAX(timestamp)
                                    FROM tells
                                    WHERE id = t.id
                                            AND owner = t.owner)
                    ORDER BY created_at''')
        c: sqlite3.Cursor = self.con.cursor()
        c.execute(f'''SELECT
                        timestamp, id, post_type, answer, likes_count, created_at, tell, owner
                    FROM tells t
                    WHERE owner = ?
                    {f'AND timestamp >= ? ' if _from is not None else ''}
                    {f'AND timestamp <= ? ' if _to is not None else ''}
                    AND timestamp = (SELECT MAX(timestamp)
                                    FROM tells
                                    WHERE id = t.id
                                            AND owner = t.owner)
                    ORDER BY created_at''',
                  (user.id,) + ((_from.isoformat(),) if _from else ()) + ((_to.isoformat(),) if _to else ()))
        x = c.fetchall()
        return [Info(TellonymTell(
            *row[1:4],
            datetime.fromisoformat(row[5]),
            *row[6],
            self.get_user(row[7]),)) for row in x]
