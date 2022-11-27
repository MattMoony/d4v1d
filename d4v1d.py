#!/usr/bin/env python3

"""
d4v1d.py - A social-media *social-engineering* tool
"""

import cmd
import utils
import config

def main():
    """
    The main entry point of the program
    """
    print(utils.title('d4v1d'))
    cmd.start()

if __name__ == '__main__':
    main()