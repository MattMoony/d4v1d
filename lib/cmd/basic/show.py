import colorama as cm
cm.init()
from lib.misc import print_err, print_inf
from lib import db, bot, platforms
from lib.bot.group import BotGroup
from nubia import command, argument, context

@command('show', aliases=['display',])
class Show(object):
    """Show information about an attribute"""

    def __init__(self) -> None:
        pass

    @command
    def platforms(self) -> None:
        """List all supported social-media platforms"""
        if not platforms.PLATFORMS:
            print_inf('Sorry... seems like no platform are available ... ')
            return
        print('PLATFORMS')
        print('    - '+'\n    - '.join(f'{p.name} ({p.link})' for p in platforms.PLATFORMS))

    @command
    def groups(self) -> None:
        """List all configured bot groups"""
        if not bot.GROUPS:
            print_inf('No bot-groups have been configured ... ')
            return
        print('BOT-GROUPS:')
        print('    - '+'\n    - '.join(str(b) for b in bot.GROUPS))

    @command
    def dbs(self) -> None:
        """List all configured db controllers"""
        if not db.CONTROLLERS:
            print_inf('No DB controllers have been configured ... ')
            return
        print('DB Controllers:')
        print('    '+'\n    '.join(f'{i:02d}: {c}' for i, c in enumerate(db.CONTROLLERS)))

    @command
    @argument('name', name='group', description='Name of the bot-group', positional=True)
    def bots(self, name: str) -> None:
        """List all configured bots in a bot group"""
        group: BotGroup = bot.group(name)
        if not group:
            print_err('bot-group', 'No group with that name!')
            return
        elif not group.bots:
            print_inf('The group doesn\'t have any configured bots ... ')
            return
        print(f'Bots in "{name}"')
        print('    '+'\n    '.join(f'{i:02d}: {b}' for i, b in enumerate(group.bots)))
