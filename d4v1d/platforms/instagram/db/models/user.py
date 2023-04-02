"""
Defines the attribute of an Instagram user 
account.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

from d4v1d.platforms.platform.user import User


@dataclass(init=False)
class InstagramUser(User):
    """
    Represents an Instagram user account.
    """

    id: int
    """The instagram user id"""
    fbid: int
    """The facebook user id"""
    full_name: str
    """The user's full name"""
    private: bool
    """Is this a private profile?"""
    category_name: Optional[str] = None
    """Name of the category, to which this "business" belongs"""
    pronouns: str = ''
    """The user's pronouns"""

    def __init__(self, id: int, fbid: int, username: str,  # pylint: disable=redefined-builtin
                 full_name: str, bio: str, no_followers: int,
                 no_following: int, profile_pic: str, private: bool,
                 number_posts: int, category_name: Optional[str] = None,
                 pronouns: str = ''):
        """
        Create a new user with the given info
        """
        super().__init__(username, bio, no_followers, no_following, number_posts, profile_pic)
        # TODO: auto-generate init with dataclass - needs
        # some extra config tho, because of alphabetical ordering
        # of arguments, etc.
        # TODO: also, adjust order of parameters to better
        # fit to the parent class it's inheriting from ...
        self.id = id
        self.fbid = fbid
        self.full_name = full_name
        self.private = private
        self.category_name = category_name
        self.pronouns = pronouns

    def dumpj(self) -> Dict[str, Any]:
        """
        Dump the user as a JSON object
        """
        return {
            'id': self.id,
            'fbid': self.fbid,
            'username': self.username,
            'full_name': self.full_name,
            'bio': self.description,
            'no_followers': self.number_followers,
            'no_following': self.number_following,
            'profile_pic': self.profile_pic,
            'private': self.private,
            'number_posts': self.number_posts,
            'category_name': self.category_name,
            'pronouns': self.pronouns,
        }

    def dumpt(self) -> Tuple[Any, ...]:
        """
        Return the user as a tuple
        """
        return (self.id, self.fbid, self.username, self.full_name,
                self.description, self.number_followers, self.number_following,
                self.profile_pic, self.private, self.number_posts,
                self.category_name, self.pronouns)

    def __str__(self):
        """
        String representation of this user
        """
        return f'InstagramUser({self.username}#{self.id})'

    @classmethod
    def loadj(cls, obj: Dict[str, Any], api: bool = False, profile_pic: Optional[str] = None) -> "InstagramUser":
        """
        Load a user from a JSON object

        Args:
            obj: The JSON object
            api: Parsing the API response?
            profile_pic: The path to the profile picture (if this is an API response)
        """
        if api:
            return InstagramUser(obj['id'], obj['fbid'], obj['username'],
                        obj['full_name'], obj['biography'], obj['edge_followed_by']['count'],
                        obj['edge_follow']['count'], profile_pic, obj['is_private'],
                        obj['edge_owner_to_timeline_media']['count'],
                        obj['category_name'], '/'.join(obj['pronouns']))
        return InstagramUser(obj['id'], obj['fbid'], obj['username'],
                    obj['full_name'], obj['bio'], obj['no_followers'],
                    obj['no_following'], obj['profile_pic'], obj['private'],
                    obj['number_posts'], obj['category_name'], obj['pronouns'])

    @classmethod
    def loadt(cls, obj: Tuple[Any, ...]) -> "InstagramUser":
        """
        Load a user from a tuple
        """
        return InstagramUser(*obj)
