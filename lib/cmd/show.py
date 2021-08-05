from nubia import command, argument, context

@command('show', aliases=['display',])
class Show(object):
    """Show information about an attribute"""

    def __init__(self) -> None:
        pass

    @command
    def user(self) -> None:
        """Show info about the current user"""
        print('show user')