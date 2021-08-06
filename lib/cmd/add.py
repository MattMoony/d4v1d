import colorama as cm
cm.init()
from lib.misc import print_err, print_inf
from lib import db, bot, platforms
from lib.bot.group import BotGroup
from nubia import command, argument, context

@command('add', aliases=['new',])
class Add(object):
    """Add/configure new objects, attributes, etc."""

    def __init__(self) -> None:
        pass

    @command
    @argument('name', description='Name of the bot-group', positional=True)
    @argument('platform', description='Name of the platform', positional=True, choices=list(map(lambda p: p.name, platforms.PLATFORMS)))
    @argument('db_controller', name='db', description='Index of the DB controller', positional=True)
    def group(self, name: str, platform: str, db_controller: int) -> None:
        """Create a new bot-group"""
        if not 0 <= db_controller < len(db.CONTROLLERS):
            print_err('DB Controllers', 'Unknown db controller (index out of range)')
            return
        BotGroup(name, platforms.platform(platform), db.CONTROLLERS[db_controller])

    @command
    @argument('sort', description='The type of db controller', positional=True, choices=list(map(lambda c: c.__name__, db.CONTROLLER_TYPES)))
    def db(self, sort: str) -> None:
        """Create a new DB connector"""
        db.controller_type(sort).create()
