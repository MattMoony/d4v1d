from nubia import command, argument, context

@command('get', aliases=['crawl','gather',])
class Show(object):
    """Collect information about your target"""

    def __init__(self) -> None:
        pass

    @command
    def overview(self, username: str) -> None:
        """Get a user's account basic info"""
        pass
