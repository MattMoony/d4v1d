"""
The CLI module of the program - contains
the main entry point of the program
"""

from d4v1d import cmd, utils


def main():
    """
    The main entry point of the program
    """
    print(utils.title('d4v1d'))
    cmd.start()

if __name__ == '__main__':
    main()
