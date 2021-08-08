"""Contains all errors that can occur"""

from typing import *

class UnknownUserError(Exception):
    """Thrown, when a user doesn't exist on a platform"""
    pass

class LoginFailedError(Exception):
    """Thrown, when a login fails"""
    pass
