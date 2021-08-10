#!/usr/bin/env python3

import os, sys, threading
import lib.cmd.basic
from lib import misc, bot
from server import server
from nubia import Nubia, Options
from argparse import ArgumentParser
from lib.cmd.plugin import D4v1dNubiaPlugin

def main():
    parser = ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', help='Debug mode?')
    args = parser.parse_args()

    # server.run(args.debug)
    # cmd.clear()
    try:
        misc.print_title("""
██████╗ ██╗  ██╗██╗   ██╗ ██╗██████╗ 
██╔══██╗██║  ██║██║   ██║███║██╔══██╗
██║  ██║███████║██║   ██║╚██║██║  ██║
██║  ██║╚════██║╚██╗ ██╔╝ ██║██║  ██║
██████╔╝     ██║ ╚████╔╝  ██║██████╔╝
╚═════╝      ╚═╝  ╚═══╝   ╚═╝╚═════╝ 
        """)
    except:
        pass
    # try:
    #     code = cmd.SUCCESS
    #     while code != cmd.CLOSING:
    #         code = cmd.handle(misc.prompt(cmd.__bot), args.debug)
    #     # else:
    #     #     server.stop()
    # except KeyboardInterrupt:
    #     print()
    #     # server.stop()
    #     cmd.__cleanup()
    # cmd.clear()

    shell = Nubia(
        name='d4v1d',
        command_pkgs=lib.cmd.basic,
        plugin=D4v1dNubiaPlugin(),
    )
    sys.exit(shell.run())

if __name__ == '__main__':
    main()