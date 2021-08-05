"""Contains all errors that can occur"""

from typing import *

class UnknownUserException(Exception):
    """Thrown, when a user doesn't exist on a platform"""
    pass

