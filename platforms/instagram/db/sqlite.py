"""
Database implementation for an SQLite database.
"""

import os
import re
import uuid
import config
import sqlite3
from log import log
from platforms.instagram.db.models import User
from platforms.instagram.db.database import Database
from platforms.instagram.db.schema.sql import SQLSchema
from typing import *

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
                log.warning(f'Database is not in a valid state - backing up to [bold]{config.PCONFIG._instagram.ddir}/{bak}.db[/bold] and creating a new database')
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
        log.debug(f'Cleaning up Instagram database ... ')
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
            for table, spec in SQLSchema.items():
                # check if the table exists
                c: sqlite3.Cursor = self.con.cursor()
                c.execute('SELECT name FROM sqlite_master WHERE type=? AND name=?', ('table', table))
                if c.fetchone() is None:
                    return False
            return True
        except Exception:
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
                log.critical(f'Crashing everything, since this shouldn\'t happen unless someone messed with the schema ([bold][red]danger of SQLi !!![/red][/bold])')
                log.critical(f'Compare your schema ("{os.path.join(os.path.dirname(__file__), "schema", "sql.py")}") with the original')
                raise ValueError(msg)
            if not re.match(__safe, table):
                # crash everything - since this should DEFINITELY
                # not happen unless someone messed with the schema
                __burn_everything_to_the_ground(table)
            if any(not (re.match(__safe, k) and (re.match(__safe, v) if type(v) == str else all(re.match(__safe, pk) for pk in v))) for k, v in spec.items()):
                __burn_everything_to_the_ground('')
            # create the table
            c: sqlite3.Cursor = self.con.cursor()
            qry: str = f'''CREATE TABLE {table} (
                {", ".join([f"{k} {v}" for k, v in spec.items() if k[0] != "."])},
                PRIMARY KEY ({", ".join(spec[".pk"])})
            )'''
            log.debug(f'Creating table [bold]{table}[/bold] using ... ')
            log.debug(qry)
            c.execute(qry)
        self.con.commit()

    def store_user(self, user: User) -> None:
        """
        Stores a user in the database

        Args:
            user (User): The user to store
        """
        c: sqlite3.Cursor = self.con.cursor()
        c.execute('''INSERT INTO users (
            id, fbid, username, full_name, bio, followers,
            following, profile_pic_local, private, category_name,
            pronouns
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )''', user.tuple())
        self.con.commit()

    def get_user(self, username: str) -> Optional[User]:
        """
        Gets a user from the database

        Args:
            username (str): The username of the user

        Returns:
            Optional[User]: The user if it exists, None otherwise
        """
        c: sqlite3.Cursor = self.con.cursor()
        c.execute('''SELECT ( 
                        id, fbid, username, full_name, bio, followers,
                        following, profile_pic_local, private, category_name,
                        pronouns
                     ) FROM users 
                     WHERE username=?''', (username,))
        row: Optional[Tuple] = c.fetchone()
        if row is None:
            return None
        return User(*row)
