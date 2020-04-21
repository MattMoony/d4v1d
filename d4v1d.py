"""The main entry point; prints the title and calls shell initialization"""

from lib import cmd
import pash.misc
import time
from argparse import ArgumentParser

def main() -> None:
    """The one and only method"""
    parser = ArgumentParser()
    parser.add_argument('fnames', type=str, help='d4v1d scripts ... ', nargs='*')
    parser.add_argument('-c', '--cmd', type=str, help='Run this command and exit ... ')
    args = parser.parse_args()

    pash.cmds.clear(None, [])
    pash.misc.fprint("""
    ___  ____       ___    ___
    | | /   |      /  |    | |
  __| |/ /| |_   __`| |  __| |
 / _` / /_| \ \ / / | | / _` by
| (_| \___  |\ V / _| || (_| MattMoony
 \__,_|   |_/ \_/  \___/\__,_|
""")

    cmd.init()
    
    stime = time.time()
    if args.fnames:
        for name in args.fnames:
            with open(name, 'r') as f:
                cmd.parse_script(f.read())
    elif args.cmd:
        cmd.parse_script(args.cmd)
    else:
        cmd.keep_polling()
    etime = time.time()

    print('[*] Finished in %.2f seconds ... ' % (etime-stime))

if __name__ == '__main__':
    main()