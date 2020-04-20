"""
Contains all functions for interacting with the data stored locally.
"""

from lib import db, models
from typing import Union, List

def get_current_info(pk: int, uname: bool = True, bio: bool = True, url: bool = True, name: bool = True) -> List[str]:
    """Get the latest stored info about the user identified by pk"""
    con, c = db.connect()
    inf = []
    if uname:
        inf.append(db.fetchone('SELECT uname FROM unames WHERE pk = ? ORDER BY first_seen DESC', pk, con=con)[0])
    if bio:
        inf.append(db.fetchone('SELECT bio FROM bios WHERE pk = ? ORDER BY first_seen DESC', pk, con=con)[0])
    if url:
        inf.append(db.fetchone('SELECT url FROM urls WHERE pk = ? ORDER BY first_seen DESC', pk, con=con)[0])
    if name:
        inf.append(db.fetchone('SELECT name FROM names WHERE pk = ? ORDER BY first_seen DESC', pk, con=con)[0])
    db.close(con)
    return inf

def get_user_by_username(uname: str) -> Union[None, models.User]:
    """Get a user by their username."""
    con, c = db.connect()
    pk = db.fetchone('SELECT pk FROM unames WHERE uname = ? ORDER BY first_seen DESC', uname, con=con)
    if not pk:
        db.close(con)
        return None
    pk = pk[0]
    u = db.fetchone('SELECT * FROM users WHERE pk = ?', pk, con=con)
    db.close(con)
    if not u:
        return None
    inf = get_current_info(pk, False)
    if any(map(lambda i: i is None, inf)):
        return None
    return models.User(pk, uname, *inf, *u)

def get_user_by_pk(pk: int) -> models.User:
    """Get a user by their pk."""
    u = db.fetchone('SELECT * FROM users WHERE pk = ?', pk)
    if not u:
        return None
    inf = get_current_info(pk)
    if any(map(lambda i: i is None, inf)):
        return None
    return models.User(pk, *inf, *u)

def get_followers(pk: int) -> List[int]:
    """Get all followers of a user."""
    fs = db.fetchall('SELECT fpk FROM fols WHERE tpk = ? AND last_seen IS NULL', pk)
    return list(map(lambda f: f[0], fs))

def get_following(pk: int) -> List[int]:
    """Get all accounts that a user follows."""
    fs = db.fetchall('SELECT tpk FROM fols WHERE fpk = ? AND last_seen IS NULL', pk)
    return list(map(lambda f: f[0], fs))