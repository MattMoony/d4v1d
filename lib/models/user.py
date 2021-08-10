"""Contains the User class. A representation of an arbitrary social-media user."""

from lib.models.media import Media
from typing import *

class User(object):
    """A user of an arbitrary social-media platform"""

    def __init__(self, username: str, platform: str, private: bool, verified: bool, user_id: Optional[int] = None, profile_pic: Optional[Media] = None, fullname: Optional[str] = None, website: Optional[str] = None, bio: Optional[str] = None):
        self.username: str = username
        self.platform: str = platform
        self.private: bool = private
        self.verified: bool = verified
        self.id: Optional[int] = user_id
        self.profile_pic: Optional[Media] = profile_pic
        self.fullname: Optional[str] = fullname
        self.website: Optional[str] = website
        self.bio: Optional[str] = bio

    def __str__(self) -> str:
        return f'{self.username}@{self.platform}'
