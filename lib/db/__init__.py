from lib.models.user import User
from typing import *

class DBController(object):
    """Base object for all DB controllers"""

    def setup(self) -> None:
        """Sets up all required db structures (tables, etc.)"""
        raise NotImplementedError()

    def get_platform(self, pid: Optional[int] = None, name: Optional[str] = None) -> Tuple[int, str, str]:
        """Gets the id, name and link of a platform"""
        raise NotImplementedError()

    def user_exists(self, pid: int, username: str) -> bool:
        """Checks, whether or not the user on the given platform is already part of the db"""
        raise NotImplementedError()
    
    def store_user(self, user: User) -> None:
        """Stores a basic overview of a social-media user in the DB"""
        raise NotImplementedError()
