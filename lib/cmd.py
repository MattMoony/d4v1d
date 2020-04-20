"""Contains the code for the shell that will be presented to the user."""

from lib.api import private
import pash.shell, pash.cmds
import pash.command as pcmd
import colorama as cr
cr.init()
from typing import List

"""The basic prompt for the d4v1d shell"""
BPROMPT: str = cr.Fore.LIGHTBLUE_EX + 'd4v1d' + cr.Fore.LIGHTBLACK_EX + '$ ' + cr.Fore.RESET
"""The shell itself"""
sh: pash.shell.Shell = pash.shell.Shell(prompt=BPROMPT)
"""The main botnet"""
bn: private.BotNet = private.BotNet(nload=True)

# =============================================================================================================================== #

def on_hello(cmd: pcmd.Command, args: List[str]) -> None:
    """Callback for the `hello` command."""
    print(' Hello World!')

def on_exit(cmd: pcmd.Command, args: List[str]) -> None:
    """Callback for `exit` - exits the shell"""
    bn.stop()
    sh.exit()

def on_login(cmd: pcmd.Command, args: List[str]) -> None:
    """Callback for `login` - creates a new bot and places it in the botnet"""
    bn.add()

def on_show_bots(cmd: pcmd.Command, args: List[str]) -> None:
    """Callback for `show bots` - shows all bots currently in the main botnet"""
    if not bn.bots:
        print(' Botnet is empty at the moment ... ')
        return
    print(' Botnet: ')
    for b in bn.bots:
        print('\t-> %s' % str(b))

def on_show_queue(cmd: pcmd.Command, args: List[str]) -> None:
    """Callback for `show queue` - shows the botnet's current task queue."""
    if not bn.q:
        print(' No tasks queued at the moment.')
        return
    print(' Tasks: ')
    for t in bn.q:
        print('\t-> %s' % str(t))

def on_get_followers(cmd: pcmd.Command, args: List[str], unames: List[str]) -> None:
    """Callback for `get followers <uname> [<uname> ...]` - gets all followers and stores them in the db."""
    if not bn.bots:
        print(' Warning: No bots in botnet ... ')
    bn.get_followers(*unames)

def on_get_following(cmd: pcmd.Command, args: List[str], unames: List[str]) -> None:
    """Callback for `get following <uname> [<uname> ...]` - gets all following and stores them in the db."""
    if not bn.bots:
        print('Warning: No bots in botnet ... ')
    bn.get_following(*unames)

def on_stop_bot(cmd: pcmd.Command, args: List[str], unames: List[str]) -> None:
    st = 0
    for b in bn.bots:
        if b.user.uname in unames:
            b.stop()
            st += 1
    print(' Stopped %d bots ... ' % st)

def on_start_bot(cmd: pcmd.Command, args: List[str], unames: List[str]) -> None:
    st = 0
    for b in bn.bots:
        if b.user.uname in unames:
            b.start()
            st += 1
    print(' Started %d bots ... ' % st)

# =============================================================================================================================== #

def init() -> None:
    """Initializes the main shell (adds all the commands), the botnet, ...; should be called before calling any other of this module's functions."""
    bn.load()
    sh.add_cmd(pcmd.Command('hello', callback=on_hello, hint='Say hello!'))
    sh.add_cmd(pcmd.Command('clear', 'cls', callback=pash.cmds.clear, hint='Clear the console ... '))
    sh.add_cmd(pcmd.Command('exit', 'quit', 'bye', callback=on_exit, hint='Exit the d4v1d terminal ... '))
    sh.add_cmd(pcmd.Command('login', callback=on_login, hint='Login to an Instagram user account ... '))
    sh.add_cmd(pcmd.CascCommand('show', cmds=[
        pcmd.Command('bots', callback=on_show_bots),
        pcmd.Command('queue', callback=on_show_queue),
    ], hint='Show different configs/states ... '))

    get_followers = pcmd.Command('followers', 'fers', callback=on_get_followers, hint='Get a user\'s followers ... ')
    get_followers.add_arg('unames', type=str, nargs='*', help='The target user\'s/users\' username(s) ... ')
    get_following = pcmd.Command('following', 'fing', callback=on_get_following, hint='Get a user\'s following-connections ... ')
    get_following.add_arg('unames', type=str, nargs='*', help='The target user\'s/users\' username(s) ... ')
    sh.add_cmd(pcmd.CascCommand('get', cmds=[
        get_followers,
        get_following,
    ], hint='Get different info ... '))

    stop_bot = pcmd.Command('stop', callback=on_stop_bot, hint='Stop a bot ... ')
    stop_bot.add_arg('unames', type=str, nargs='*', help='The target bot\'s/bots\' username(s) ... ')
    sh.add_cmd(stop_bot)

    start_bot = pcmd.Command('start', callback=on_start_bot, hint='Start a bot ... ')
    start_bot.add_arg('unames', type=str, nargs='*', help='The target bot\'s/bots\' username(s) ... ')
    sh.add_cmd(start_bot)

def keep_polling() -> None:
    """Will ask the shell to keep prompting the user for commands until it exits."""
    sh.prompt_until_exit()

def parse_command(cmd: str, *args: str) -> None:
    """Will parse the given command(s)."""
    for cm in [cmd, *args]:
        sh.parse(cm)