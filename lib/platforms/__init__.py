"""Contains the base Platform class"""

import requests as req
from lib.models.user import User
from typing import *

class Platform(object):
    """Is a base class to all social-media platforms"""
    
    """Defines some social-media platform specific parameters"""
    params: Dict[str, str] = {}
    """Contains endpoints required for all interactions with the platform"""
    endpoints: Dict[str, str] = {}

    @classmethod
    def get_user_agent(cls) -> str:
        """Generates and returns the default User-Agent for the platform"""
        raise NotImplementedError()

    @classmethod
    def get_headers(cls) -> Dict[str, str]:
        """Generates and returns the default headers for the platform"""
        raise NotImplementedError()

    @classmethod
    def get_user(cls, session: req.Session, username: str, headers: Optional[Dict[str, str]] = None) -> User:
        """Gets a basic overview of a social-media user"""
        raise NotImplementedError()