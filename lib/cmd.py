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
    ], hint='Show different configs/states ... '))

def keep_polling() -> None:
    """Will ask the shell to keep prompting the user for commands until it exits."""
    sh.prompt_until_exit()