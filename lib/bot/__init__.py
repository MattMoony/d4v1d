"""Exposes an array of all active botgroups"""

from .bot import *
from .group import *
from typing import *

"""A list of all currently active bot groups"""
GROUPS: List[BotGroup] = []

def group(name: str) -> Optional[BotGroup]:
    """Get an active group by its name"""
    try:
        return next(filter(lambda g: g.name == name, GROUPS))
    except StopIteration:
        return None
