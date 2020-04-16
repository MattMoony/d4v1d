"""Definitions of all model classes are here."""

from lib import tmp, db
from lib.api import params
import time, datetime, os
from typing import Any, Optional
import requests as req
import pash.misc

class User(object):
    """
    Represents an Instagram user.

    ...

    Attributes
    ----------
    pk : int
        The user-id (private key?!).
    uname : str
        The username.
    bio : str
        The user's biography.
    url : str
        The external URL the user has specified.
    name : str
        The user's full name.
    business : bool
        Whether or not the user is a business account.
    private : bool
        Whether or not the user is private.
    verified : bool
        Whether or not the user is verified.
    ppic : str
        The URL to the HD version of the user's profile pic.
    followers : str
        The amount of followers the user has.
    following : int
        The amount of people the user follows.
    raw : Any
        The raw response from which this information was extracted.

    Methods
    -------
    store()
        Will store/update all the user's attributes in the sqlite database file.
    __str__()
        Gives a nice, short string representation of the user.
    """

    def __init__(self, pk: int, uname: str, bio: str, url: str, name: str, business: bool, 
                 private: bool, verified: bool, ppic: str, followers: int, following: int, raw: Any = None) -> None:
        """
        Parameters
        ----------
        pk : int
            The user-id (private key?!)
        uname : str
            The username.
        bio : str
            The user's biography.
        url : str
            The user's external URL.
        name : str
            The user's full name.
        business : bool
            Whether or not the user has a business account.
        private : bool
            Whether or not the user is private.
        verified : bool
            Whether or not the user is verified.
        ppic : str
            The link to the HD version of the user's profile pic.
        followers : int
            The amount of followers the user has.
        following : int
            The amount of people the user follows.
        raw : Any
            The raw response from which this info was extracted. Default is None.
        """
        self.pk: int = pk
        self.uname: str = uname
        self.bio: str = bio
        self.url: str = url
        self.name: str = name
        self.business: str = business
        self.private: bool = private
        self.verified: bool = verified
        self.ppic: str = ppic
        self.followers: int = followers
        self.following: int = following
        self.raw: Any = raw
        self.store()

    def store(self) -> None:
        """Stores/updates all the user's information in the sqlite database."""
        if not db.exists('SELECT * FROM users WHERE pk = ?', self.pk):
            db.exec('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)', self.pk, self.business, self.private, self.verified, self.followers, self.following)
        else:
            db.exec('UPDATE users SET business=?,private=?,verified=?,followers=?,following=? WHERE pk=?', 
                    self.business, self.private, self.verified, self.followers, self.following, self.pk)
        db.update_if_necessary(self.pk, 'first_seen', dict(bios=('bio',self.bio), names=('name',self.name), unames=('uname',self.uname), urls=('url',self.url)))

    def __str__(self) -> str:
        """Gives a short string representation of the Instagram user."""
        if self.name:
            return '{} ({})'.format(self.name, self.uname)
        return self.uname

class Post(object):
    """
    Represents an Instagram post.

    ...

    Attributes
    ----------
    user : User
        The poster.
    id : str
        The post's unique id.
    shortcode : str
        The post's shortcode.
    url : str
        URL to the image.
    created_at : int
        Timestamp of when the post was uploaded.
    caption : str
        The post's caption.
    likes : int
        The amount of likes the post has.
    location : str
        The post's location (if any).

    Methods
    -------
    store()
        Stores/updates all information about the post in the sqlite db.
    """

    def __init__(self, user : User, id : str, shortcode: str, url: str, created_at: int, caption: str, likes: int, location: str) -> None:
        """
        Parameters
        ----------
        user : User
            The poster.
        id : str
            The post's unique id.
        shortcode : str
            The post's shortcode.
        url : str
            URL to the image.
        created_at : int
            Timestamp of when the post was uploaded.
        caption : str
            The post's caption.
        likes : int
            The amount of likes the post has.
        location : str
            The post's location (if any).
        """
        self.user: User = user
        self.id: str = id
        self.shortcode: str = shortcode
        self.url: str = url
        self.created_at: int = created_at
        self.caption: str = caption
        self.likes: int = likes
        self.location: str = location
        self.store()

    def store(self) -> None:
        """Stores/updates all information about the post in the sqlite db."""
        if not db.exists('SELECT * FROM posts WHERE id = ?', self.id):
            db.exec('INSERT INTO posts VALUES (?, ?, ?, ?, ?, ?, ?, ?)', self.user.pk, self.id, self.shortcode, self.created_at, datetime.datetime.now(), self.caption, self.likes, self.location)
        else:
            db.exec('UPDATE posts SET last_seen=?, likes=? WHERE id=?', datetime.datetime.now(), self.likes, self.id)
            if self.caption:
                db.exec('UPDATE posts SET caption=? WHERE id=?', self.caption, self.id)
            if self.location:
                db.exec('UPDATE posts SET location=? WHERE id=?', self.location, self.id)
        dst = os.path.join(params.TMP_PATH, self.user.uname)
        fname = os.path.join(dst, '{}.jpg'.format(self.id))
        if not os.path.isdir(dst):
            os.makedirs(dst)
        res = req.get(self.url, stream=True)
        pb = pash.misc.ProgressBar(int(res.headers['Content-length']), 'Downloading https://www.instagram.com/p/{} '.format(self.shortcode))
        try:
            with open(fname, 'wb') as im:
                for ch in res:
                    pb.inc(len(ch))
                    im.write(ch)
        except Exception:
            pb.ensure_end()
            print(' Download interrupted! Removing file ... ')
            if os.path.isfile(fname):
                os.remove(fname)
            return
        pb.ensure_end()

    def __str__(self) -> str:
        return 'https://www.instagram.com/p/{}'.format(self.shortcode)