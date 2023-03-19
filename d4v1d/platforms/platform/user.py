"""
A sort of abstract base class for social-media
platform users that isn't really abstract tho.
It's used for the cross-platform commands to
abstract users from several platforms and keep
only shared aspects.
"""

from typing import List, Optional
from dataclasses import dataclass

from d4v1d.platforms.platform.info import Info

@dataclass
class User:
    """
    A sort of abstract base class for social-media
    platform users that isn't really abstract tho.
    It's used for the cross-platform commands to
    abstract users from several platforms and keep
    only shared aspects.
    """

    username: str
    """The user's username."""
    description: str
    """The user's description/bio."""
    number_followers: int
    """The user's number of followers."""
    number_following: int
    """The number of people the user follows."""
    number_posts: int
    """The number of posts the user has made."""
    profile_pic: str
    """Path to the profile pic (local)."""

    followers: Optional[Info[List["User"]]] = None
    """The user's followers. Seems redundant - exists for performance optimization."""
    following: Optional[Info[List["User"]]] = None
    """The people the user follows. Seems redundant - exists for performance optimization."""
