"""
Module containing all database interfaces that are
supported by the crawler for this social-media platform.
Plus the base class that all interfaces extend. 
"""

from typing import *

from d4v1d.platforms.instagram.config import InstagramDBType
from d4v1d.platforms.instagram.db.database import Database
from d4v1d.platforms.instagram.db.sqlite import SQLiteDatabase

DATABASES: Dict[InstagramDBType, Type[Database]] = {
    InstagramDBType.SQLITE: SQLiteDatabase,
}
