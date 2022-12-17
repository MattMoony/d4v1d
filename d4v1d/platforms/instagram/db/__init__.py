"""
Module containing all database interfaces that are
supported by the crawler for this social-media platform.
Plus the base class that all interfaces extend. 
"""

from .database import Database
from .sqlite import SQLiteDatabase
from d4v1d.platforms.instagram.config import InstagramDBType
from typing import *

DATABASES: Dict[InstagramDBType, Type[Database]] = {
    InstagramDBType.SQLITE: SQLiteDatabase,
}
