from lib.errors import BotGroupNameTaken, LoginFailedError
import colorama as cm
cm.init()
from prompt_toolkit import prompt
from lib import db, bot, platforms
from lib.bot.group import BotGroup
from lib.misc import print_err, print_inf
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
        try:
            BotGroup(name, platforms.platform(platform), db.CONTROLLERS[db_controller])
        except BotGroupNameTaken:
            print_err('bot-groups', f'Group with the name "{name}" already exists ... ')

    @command
    @argument('sort', description='The type of db controller', positional=True, choices=list(map(lambda c: c.__name__, db.CONTROLLER_TYPES)))
    def db(self, sort: str) -> None:
        """Create a new DB connector"""
        db.controller_type(sort).create()

    @command
    @argument('group_name', name='group', description='Name of the group to add it to', positional=True)
    @argument('anonymous', description='Don\'t use an account?')
    def bot(self, group_name: str, anonymous: bool = False) -> None:
        """Create a new bot and add it to a bot-group"""
        group: BotGroup = bot.group(group_name)
        if not group:
            print_err('bot-group', 'No group with that name!')
            return
        elif anonymous:
            group.add()
            return
        username: str = prompt(f'{group.platform.name} | Username: ')
        try:
            group.add(username, 
                    prompt(f'{group.platform.name} | Password: ', is_password=True))
        except LoginFailedError:
            print_err('login', f'Login Failed for {username}@{group.platform.name}!')
