from lib import db
from lib.misc import print_err
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
