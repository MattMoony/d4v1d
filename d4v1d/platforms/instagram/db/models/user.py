"""
Defines the attribute of an Instagram user 
account.
"""

from typing import *

class User(object):
    """
    Represents an Instagram user account.
    """

    id: int
    """The instagram user id"""
    fbid: int
    """The facebook user id"""
    username: str
    """The user's username"""
    full_name: str
    """The user's full name"""
    bio: str
    """The user's bio"""
    no_followers: int
    """Number of followers"""
    no_following: int
    """Number of following"""
    profile_pic: str
    """Path to the profile picture (local)"""
    private: bool
    """Is this a private profile?"""
    number_posts: int
    """Number of posts"""
    category_name: Optional[str]
    """Name of the category, to which this "business" belongs"""
    pronouns: str
    """The user's pronouns"""

    def __init__(self, id: int, fbid: int, username: str, 
                 full_name: str, bio: str, no_followers: int, 
                 no_following: int, profile_pic: str, private: bool,
                 number_posts: int, category_name: Optional[str] = None, 
                 pronouns: str = ''):
        """
        Create a new user with the given info
        """
        self.id = id
        self.fbid = fbid
        self.username = username
        self.full_name = full_name
        self.bio = bio
        self.no_followers = no_followers
        self.no_following = no_following
        self.profile_pic = profile_pic
        self.private = private
        self.number_posts = number_posts
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
            'bio': self.bio,
            'no_followers': self.no_followers,
            'no_following': self.no_following,
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
                self.bio, self.no_followers, self.no_following, 
                self.profile_pic, self.private, self.number_posts,
                self.category_name, self.pronouns)

    def __str__(self):
        """
        String representation of this user
        """
        return f'InstagramUser({self.username}#{self.id})'

    @classmethod
    def loadj(cls, obj: Dict[str, Any], api: bool = False, profile_pic: Optional[str] = None) -> "User":
        """
        Load a user from a JSON object

        Args:
            obj: The JSON object
            api: Parsing the API response?
            profile_pic: The path to the profile picture (if this is an API response)
        """
        if api:
            return User(obj['id'], obj['fbid'], obj['username'],
                        obj['full_name'], obj['biography'], obj['edge_followed_by']['count'],
                        obj['edge_follow']['count'], profile_pic, obj['is_private'],
                        obj['edge_owner_to_timeline_media']['count'],
                        obj['category_name'], '/'.join(obj['pronouns']))
        return User(obj['id'], obj['fbid'], obj['username'], 
                    obj['full_name'], obj['bio'], obj['no_followers'], 
                    obj['no_following'], obj['profile_pic'], obj['private'], 
                    obj['number_posts'], obj['category_name'], obj['pronouns'])

    @classmethod
    def loadt(cls, obj: Tuple[Any, ...]) -> "User":
        """
        Load a user from a tuple
        """
        return User(*obj)
