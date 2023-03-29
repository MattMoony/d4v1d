"""
Defines the attribute of an Tellonym user 
account.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

from d4v1d.platforms.platform.user import User


@dataclass(init=False)
class TellonymUser(User):
    """
    Represents an Tellonym user account.
    """

    id: int
    """The tellonym user id"""

    def __init__(self, id: int, username: str, aboutMe: str, followerCount: int, followingCount: int, avatarFileName: str, tellCount: int):
        self.id = id
        self.username = username
        self.description = aboutMe
        self.number_followers = followerCount
        self.number_following = followingCount
        self.profile_pic = avatarFileName
        self.number_posts = tellCount
        pass

    def dumpj(self) -> Dict[str, Any]:
        """
        Dump the user as a JSON object
        """
        return {
            'id': self.id,
            'username': self.username,
            'aboutMe': self.description,
            'followerCount': self.number_followers,
            'followingCount': self.number_following,
            'avatarFileName': self.profile_pic,
            'tellCount': self.number_posts,
        }

    def dumpt(self) -> Tuple[Any, ...]:
        """
        Return the user as a tuple
        """
        return (
            self.id,
            self.username,
            self.description,
            self.number_followers,
            self.number_following,
            self.profile_pic,
            self.number_posts,
        )

    @classmethod
    def loadj(cls, obj: Dict[str, Any], api: bool = False, profile_pic: Optional[str] = None) -> "TellonymUser":
        """
        Load a user from a JSON object

        Args:
            obj: The JSON object
            api: Parsing the API response?
            profile_pic: The path to the profile picture (if this is an API response)
        """
        if api:
            return TellonymUser(avatarFileName=obj['avatarFileName'], followerCount=obj['followerCount'], followingCount=obj['followingCount'], id=obj['id'], username=obj['username'], aboutMe=obj['aboutMe'], tellCount=obj['tellCount'])
        return TellonymUser(**obj)

    @classmethod
    def loadt(cls, obj: Tuple[Any, ...]) -> "TellonymUser":
        """
        Load a user from a tuple
        """
        return TellonymUser(*obj)
