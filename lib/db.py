"""
All interactions with the sqlite db should involve this module's functions.
"""

from lib.api import params
import sqlite3, os
from typing import Tuple, Dict, Any, Optional, Union, List

"""Path to the sqlite db file."""
DB_PATH: str = os.path.join(params.TMP_PATH, 'info.db')

# =========================================================================================================================== #

def connect() -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    """
    Creates a connection to the sqlite db.
    
    Returns
    -------
    Tuple[sqlite3.Connection, sqlite3.Cursor]
        A tuple consisting of both the connection to the db and a cursor for the
        sqlite db.
    """
    con = sqlite3.connect(DB_PATH)
    return (con, con.cursor())

def close(con: sqlite3.Connection) -> None:
    """
    Closes the connection to the sqlite db.

    Parameters
    ----------
    con : sqlite3.Connection
        The connection to the db.
    """
    con.commit()
    con.close()

def exec(query: str, *args: Any, con: Optional[sqlite3.Connection] = None) -> None:
    """
    Opens a connection, executes the given query and closes the connection again.

    Parameters
    ----------
    query : str
        The query.
    *args : Any
        Arguments for the query (escaped parameters, i.e. '?' ...)
    con : Optional[sqlite3.Connection]
        Connection to the db.
    """
    arti = not con
    if arti:
        con, c = connect()
    else:
        c = con.cursor()
    c.execute(query, (*args, ))
    if arti:
        close(con)

def fetchone(query: str, *args: Any, con: Optional[sqlite3.Connection] = None) -> Union[Tuple[Any], None]:
    """
    Opens a connection, executes the query and returns the first result.

    Parameters
    ----------
    query : str
        The query.
    *args : Any
        Arguments for the query.
    con : Optional[sqlite3.Connection]
        Connection to the db. 
    
    Returns
    -------
    Union[Tuple[Any], None]
        Returns the first result (if any).
    """
    arti = not con
    if arti:
        con, c = connect()
    else:
        c = con.cursor()
    c.execute(query, (*args, ))
    res = c.fetchone()
    if arti:
        close(con)
    return res

def fetchall(query: str, *args: Any, con: Optional[sqlite3.Connection] = None) -> List[Tuple[Any]]:
    """
    Opens a connection, executes the query and returns all results.

    Parameters
    ----------
    query : str
        The query.
    *args : Any
        The arguments for the query.
    con : Optional[sqlite3.Connection]
        Connection to the db.
    
    Returns
    -------
    List[Tuple[Any]]
        Returns resulting rows (or empty list)
    """
    arti = not con
    if arti:
        con, c = connect()
    else:
        c = con.cursor()
    c.execute(query, (*args, ))
    res = c.fetchall()
    if arti:
        close(con)
    return res

# =========================================================================================================================== #

def exists(query: str, *args: Any, con: Optional[sqlite3.Connection] = None) -> bool:
    """
    Checks whether or not the given query yields a result.

    Parameters
    ----------
    query : str
        The query.
    *args : Any
        Arguments for the query (escaped parameters; '?' ...)
    con : Optional[sqlite3.Connection]
        Connection to the db.

    Returns
    -------
    bool
        Whether or not the query has yielded a result.
    """
    arti = not con
    if arti:
        con, c = connect()
    else:
        c = con.cursor()
    c.execute(query, (*args, ))
    res = bool(c.fetchone())
    if arti:
        close(con)
    return res

def update_if_necessary(pk: int, col: str, tbls: Dict[str, Tuple[str, Any]], con: Optional[sqlite3.Connection] = None) -> None:
    """
    Useful for keeping track of changing parameters over time. Will search the database
    for the latest entries of the given parameters and create a new one, in case the given
    parameter has changed.

    Parameters
    ----------
    pk : int
        The private key (user-id) of the target user. (for whom the parameters should be checked)
    col : str
        The name of the column that contains the parameter to sort by (probably of type DATETIME).
    tbls : Dict[str, Tuple[str, Any]]
        Key --> name of the table. Tuple[0] --> name of the column that contains the critical parameter.
        Tuple[1] --> the current value of that parameter (the one, the old one should be compared to).
    con : Optional[sqlite3.Connection]
        Connection to the db.
    """
    arti = not con
    if arti:
        con, c = connect()
    else:
        c = con.cursor()
    for k, v in tbls.items():
        c.execute('SELECT "{}" FROM "{}" WHERE pk = ? ORDER BY "{}" DESC LIMIT 1'.format(v[0], k, col), (pk, ))
        r = c.fetchone()
        if not r or r[0] != v[1]:
            c.execute('INSERT INTO "{}" (pk,"{}") VALUES (?,?)'.format(k, v[0]), (pk, v[1], ))
    if arti:
        close(con)

# =========================================================================================================================== #