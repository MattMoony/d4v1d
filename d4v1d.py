"""The main entry point; prints the title and calls shell initialization"""

from lib import cmd
import pash.misc

def main() -> None:
    """The one and only method"""
    pash.misc.fprint("""
    ___  ____       ___    ___
    | | /   |      /  |    | |
  __| |/ /| |_   __`| |  __| |
 / _` / /_| \ \ / / | | / _` by
| (_| \___  |\ V / _| || (_| MattMoony
 \__,_|   |_/ \_/  \___/\__,_|
""")

    cmd.init()
    cmd.keep_polling()

if __name__ == '__main__':
    main()