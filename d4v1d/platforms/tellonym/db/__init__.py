"""
Module containing all database interfaces that are
supported by the crawler for this social-media platform.
Plus the base class that all interfaces extend. 
"""

from typing import *

from d4v1d.platforms.tellonym.config import TellonymDBType
from d4v1d.platforms.tellonym.db.database import Database
from d4v1d.platforms.tellonym.db.sqlite import SQLiteDatabase

DATABASES: Dict[TellonymDBType, Type[Database]] = {
    TellonymDBType.SQLITE: SQLiteDatabase,
}
