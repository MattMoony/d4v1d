from nubia import command, argument, context

@command('get', aliases=['crawl','gather',])
class Show(object):
    """Collect information about your target"""

    def __init__(self) -> None:
        pass

    @command
    @argument('group_name', name='group', description='The bot-group that should execute the command', positional=True)
    @argument('username', description='The target username', positional=True)
    def overview(self, group_name: str, username: str) -> None:
        """Get a user's account basic info"""
        pass
