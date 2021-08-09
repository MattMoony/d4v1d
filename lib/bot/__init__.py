"""Exposes an array of all active botgroups"""

import os, json
import lib.params
from lib.misc import print_wrn

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

def reset_config():
    """Reset the configuration stored on the hard disk"""
    with open(os.path.join(lib.params.LIB_PATH, 'bot', 'groups.json'), 'w') as f:
        json.dump([], f)

def write_config():
    """Write the configuration for the current bot-groups to disk"""
    with open(os.path.join(lib.params.LIB_PATH, 'bot', 'groups.json'), 'w') as f:
        json.dump([g.json() for g in GROUPS], f)

def init():
    """Initializes the GROUPS list with the values stored on the hard disk"""
    global GROUPS
    group_p: str = os.path.join(lib.params.LIB_PATH, 'bot', 'groups.json')
    if not os.path.isfile(group_p):
        reset_config()
        return
    with open(group_p, 'r') as f:
        try:
            groups: List[Dict[str, Any]] = json.load(f)
            if type(groups) != list:
                raise json.decoder.JSONDecodeError()
        except json.decoder.JSONDecodeError:
            print_wrn('Corrupted bot-groups config', 'Resetting it ... ')
            reset_config()
            return
        for g in groups:
            BotGroup.unjson(g)

def register_group(g: BotGroup) -> None:
    """Registers a new bot-group, both in memory and on disk"""
    global GROUPS
    if g not in GROUPS:
        GROUPS.append(g)
        write_config()

if __name__ != '__main__':
    init()
