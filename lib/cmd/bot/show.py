import colorama as cm
cm.init()
from lib.misc import print_err, print_inf
from lib import bot, cmd
from lib.bot import Bot, BotGroup
from nubia import command, argument, context
from typing import *

@command('show', aliases=['display',])
class Show(object):
    """Show information about an attribute"""

    def __init__(self) -> None:
        pass

    @command
    def queue(self) -> None:
        """List all queued tasks"""
        with cmd.BOT_GROUP.tasks_lock:
            if not cmd.BOT_GROUP.tasks:
                print_inf('No tasks in queue ... ')
                return
            print('QUEUED TASKS')
            print('    - '+'\n    - '.join(f'{t[0].__name__}({", ".join(t[1])})' for t in cmd.BOT_GROUP.tasks))
    
    @command
    def tasks(self) -> None:
        """List all currently running tasks"""
        tasks: List[Tuple[Bot, Tuple[Tuple[Callable, List[Any], Dict[str, Any], Optional[Callable]]]]] = []
        with cmd.BOT_GROUP.bots_lock:
            for b in cmd.BOT_GROUP.bots:
                with b.occupied_lock:
                    if b.task:
                        tasks.append((b, b.task))
        if not tasks:
            print_inf('No tasks are currently being worked on ... ')
            return
        print('RUNNING TASKS')
        print('    . '+'\n    . '.join(f'{b} - {t[0].__name__}({", ".join(t[1])})' for b, t in tasks))
    