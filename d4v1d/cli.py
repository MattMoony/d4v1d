"""
The CLI module of the program - contains
the main entry point of the program
"""

from argparse import ArgumentParser

from d4v1d import cmd, utils


def main():
    """
    The main entry point of the program
    """
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument('cmds', nargs='*')
    args = parser.parse_args()

    print(utils.title('d4v1d'))
    cmd.start(args.cmds)

if __name__ == '__main__':
    main()
