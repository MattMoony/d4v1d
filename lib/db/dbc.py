from lib.models import User, Media
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

    def __store_user(self, username: str, pid: int, user_id: int, *args: List[Any]) -> None:
        """Only store the most essential information"""
        raise NotImplementedError()
    
    def store_user(self, user: User) -> None:
        """Stores a basic overview of a social-media user in the DB"""
        raise NotImplementedError()

    def get_user(self, username: str, pid: int) -> User:
        """Loads and returns a user from the database"""
        raise NotImplementedError()

    def store_media_snapshot(self, username: str, pid: int) -> int:
        """Creates a new media snapshot entry and returns the timestamp"""
        raise NotImplementedError()

    def store_media(self, user: User, pid: int, timestamp: int, media: Media) -> None:
        """Stores a media entry in the db"""
        raise NotImplementedError()

    def __store_tagged(self, username: str, pid: int, timestamp: int, name: str, tagged: User, *args: List[Any]) -> None:
        """Method called by store_tagged"""
        raise NotImplementedError()

    def store_tagged(self, username: str, pid: int, timestamp: int, name: str, tagged: User) -> None:
        """Stores a user that has been tagged in media in the db"""
        raise NotImplementedError()
