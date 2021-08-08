from lib import cmd
from lib.bot import Bot
from nubia import command, argument, context

@command('get', aliases=['crawl','gather',])
class Show(object):
    """Collect information about your target"""

    def __init__(self) -> None:
        pass

    @command
    @argument('username', description='The target username', positional=True)
    def overview(self, username: str) -> None:
        """Get a user's account basic info"""
        cmd.BOT_GROUP.run(Bot.get_user, username)
