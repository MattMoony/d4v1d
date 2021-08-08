from lib import db, bot
from lib.misc import print_err
from lib.bot.group import BotGroup
from nubia import command, argument, context

@command('rm', aliases=['remove', 'delete',])
class Add(object):
    """Remove objects/attributes, etc."""

    def __init__(self) -> None:
        pass

    @command
    @argument('db_controller', name='db', description='Index of the DB controller', positional=True)
    def db(self, db_controller: int) -> None:
        """Remove a configured db controller"""
        if not 0 <= db_controller < len(db.CONTROLLERS):
            print_err('DB Controllers', 'Unknown db controller (index out of range)')
            return
        del db.CONTROLLERS[db_controller]
        db.write_config()

    @command
    @argument('group_name', name='group', description='The name of the bot-group', positional=True)
    @argument('idx', name='index', description='Index of the bot to remove', positional=True)
    def bot(self, group_name: str, idx: int) -> None:
        """Remove a bot from a bot-group"""
        group: BotGroup = bot.group(group_name)
        if not group:
            print_err('bot-group', 'No group with that name!')
            return
        elif not 0 <= idx < len(group.bots):
            print_err('bot-group', f'Bot index out of range ([0;{len(group.bots)}[)')
            return
        group.remove(idx)
