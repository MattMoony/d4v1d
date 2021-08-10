"""Contains the base Platform class"""

from lib.platforms.platform import Platform
from lib.platforms.instagram import Instagram
from typing import *

"""A list of all supported social-media platforms"""
PLATFORMS: List[Type] = [ Instagram, ]

def platform(name: str) -> Optional[Type]:
    """Get a platform by its name"""
    try:
        return next(filter(lambda p: p.name == name, PLATFORMS))
    except StopIteration:
        return None
