import os
from lib import misc, bot, cmd
from argparse import ArgumentParser

def main():
    parser = ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', help='Debug mode?')
    args = parser.parse_args()

    cmd.clear()
    misc.print_title("""
██████╗ ██╗  ██╗██╗   ██╗ ██╗██████╗ 
██╔══██╗██║  ██║██║   ██║███║██╔══██╗
██║  ██║███████║██║   ██║╚██║██║  ██║
██║  ██║╚════██║╚██╗ ██╔╝ ██║██║  ██║
██████╔╝     ██║ ╚████╔╝  ██║██████╔╝
╚═════╝      ╚═╝  ╚═══╝   ╚═╝╚═════╝ 
    """)
    try:
        code = cmd.SUCCESS
        while code != cmd.CLOSING:
            code = cmd.handle(misc.prompt(cmd.__bot), args.debug)
    except KeyboardInterrupt:
        print()
        cmd.__cleanup()
    cmd.clear()

if __name__ == '__main__':
    main()