"""
The CLI module of the program - contains
the main entry point of the program
"""

import d4v1d.cmd as cmd
import d4v1d.utils as utils
import d4v1d.config as config

def main():
    """
    The main entry point of the program
    """
    print(utils.title('d4v1d'))
    cmd.start()

if __name__ == '__main__':
    main()