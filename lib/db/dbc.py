from lib.models.user import User
from typing import *

class DBController(object):
    """Base object for all DB controllers"""

    def __eq__(self, other: Any) -> bool:
        if type(self) != type(other):
            return False
        return self.json() == other.json()

    @classmethod
    def create(cls) -> "DBController":
        """Create a new DB Controller interactively"""
        raise NotImplementedError()

    @classmethod
    def unjson(cls, json: Dict[str, Any]) -> "DBController":
        """Create a new DB Controller based on the given configuration"""
        raise NotImplementedError()

    def setup(self) -> None:
        """Sets up all required db structures (tables, etc.)"""
        raise NotImplementedError()

    def json(self) -> Dict[str, Any]:
        """Converts the DBController's configuration to a dictionary"""
        raise NotImplementedError()

    def healthy(self) -> bool:
        """Confirm that the db controller's db is still healthy and operational"""
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
