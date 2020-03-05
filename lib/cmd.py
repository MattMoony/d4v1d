import os, argparse, traceback, datetime, time, json
from lib import misc, bot, api, params
from selenium import webdriver
import colorama as cm
cm.init()

# -- UTILS ----------------------------------------------------------------------------------------------------------------------------------------------- #

class ArgumentParser(argparse.ArgumentParser):
    def error(self, msg):
        print(' %s' % msg)
        raise argparse.ArgumentError()

# -- FUNCTIONS ------------------------------------------------------------------------------------------------------------------------------------------- #

def clear(*args):
    os.system('clear' if os.name == 'posix' else 'cls')
    return SUCCESS

def bye(*args):
    return CLOSING

def login(*args):
    global __bot
    if len(args) > 1:
        if args[1] in ('renew', 'r'):
            __bot = bot.Bot(cache=False)
        elif args[1] in ('help', '?'):
            misc.print_dict('Help: "{} [<opt.>]'.format(args[0]), HELP['login']['opts'])
        else:
            misc.print_err(args[0], 'Unknown option "{}"'.format(args[1]))
            return FAILURE
    else:
        __bot = bot.Bot()
    if __bot and not __bot.cookies:
        misc.print_err('Bot', 'Creation failed!')
        __bot = None
        return FAILURE
    return SUCCESS

def logout(*args):
    global __bot, __driver
    __bot = None
    if __driver:
        __driver.quit()
        __driver = None
    return SUCCESS

def show(*args):
    if len(args) < 2:
        misc.print_err(args[0], 'Missing arguments "{} <opt.>"'.format(args[0]))
        return FAILURE
    elif args[1] in ('u', 'user'):
        if __bot:
            misc.print_dict('Current User', { 'Username': __bot.user['username'], 'User-ID': __bot.user['pk'], })
        else:
            print(' Not logged in!')
            return FAILURE
    elif args[1] in ('h', 'headers'):
        if __bot:
            misc.print_dict('Header-Config.', __bot.headers)
        else:
            print(' Not configured. Try logging in!')
            return FAILURE
    elif args[1] in ('a', 'user-agent'):
        if __bot:
            misc.print_dict('Header-Config.', { 'User-Agent': __bot.headers['User-Agent'], })
        else:
            print(' Not configured. Try logging in!')
            return FAILURE
    elif args[1] in ('c', 'cookies'):
        if __bot:
            misc.print_dict('Cookies', { k: v['value'] for k, v in __bot.cookies.items() })
        else:
            print(' None set. Try logging in!')
    elif args[1] in ('help', '?'):
        misc.print_dict('Help: "{} <opt.>"'.format(args[0]), HELP['show, display, sh, disp']['opts'])
    else:
        misc.print_err(args[0], 'Unkown option "{}"'.format(args[1]))
        return FAILURE
    return SUCCESS

def get(*args):
    if len(args) < 2:
        misc.print_err(args[0], 'Missing arguments "{} <opt.>"'.format(args[0]))
        return FAILURE
    elif args[1] in ('v', 'overview'):
        parser = ArgumentParser()
        parser.add_argument('user', help='Specifies the target username ... ')
        try:
            args = parser.parse_args(args[2:])
            misc.print_dict('Overview: {}'.format(args.user), { k.title().replace('_', ' '): v for k, v in api.get_user_overview(args.user, headers=__bot.headers if __bot else {}).items()})
        except argparse.ArgumentError:
            return FAILURE
    elif args[1] in ('o', 'followers'):
        if not __bot:
            print(' You need to be logged in!')
            return FAILURE
        parser = ArgumentParser()
        parser.add_argument('user', help='Specifies the target username ... ')
        parser.add_argument('-d', '--dest', help='Specifies the output directory ...', default=None)
        try:
            args = parser.parse_args(args[2:])
            args.dest = args.dest or os.path.abspath(os.path.join(params.TMP_PATH, '{}/o{}'.format(args.user, str(time.time()))))
            if not os.path.isdir(args.dest):
                os.makedirs(args.dest)
            fs = __bot.get_followers(api.get_userid(args.user))
            p = os.path.abspath(os.path.join(args.dest, 'followers.json'))
            print(' Storing in "%s" ... ' % p)
            with open(p, 'w') as f:
                json.dump(fs, f, indent=4, sort_keys=True)
        except argparse.ArgumentError:
            return FAILURE
    elif args[1] in ('i', 'following'):
        if not __bot:
            print(' You need to be logged in!')
            return FAILURE
        parser = ArgumentParser()
        parser.add_argument('user', help='Specifies the target username ... ')
        parser.add_argument('-d', '--dest', help='Specifies the output directory ...', default=None)
        try:
            args = parser.parse_args(args[2:])
            args.dest = args.dest or os.path.abspath(os.path.join(params.TMP_PATH, '{}/i{}'.format(args.user, str(time.time()))))
            if not os.path.isdir(args.dest):
                os.makedirs(args.dest)
            fs = __bot.get_following(api.get_userid(args.user))
            p = os.path.abspath(os.path.join(args.dest, 'following.json'))
            print(' Storing in "%s" ... ' % p)
            with open(p, 'w') as f:
                json.dump(fs, f, indent=4, sort_keys=True)
        except argparse.ArgumentError:
            return FAILURE
    elif args[1] in ('m', 'media'):
        parser = ArgumentParser()
        parser.add_argument('user', help='Specifies the target username ... ')
        parser.add_argument('-d', '--dest', help='Specifies the output directory ...', default=None)
        try:
            args = parser.parse_args(args[2:])
            api.get_media(args.user, args.dest, __bot.session if __bot else None)
        except argparse.ArgumentError:
            return FAILURE

    elif args[1] in ('?', 'help'):
        misc.print_dict('Help: "{} <opt.>"'.format(args[0]), HELP['get, dump']['opts'])
    else:
        misc.print_err(args[0], 'Unknown option "{}"'.format(args[1]))
    return SUCCESS

def man(*args):
    global __driver
    if __driver:
        __driver.quit()
    __driver = webdriver.Firefox()
    __driver.get('https://instagram.com/')
    if __bot:
        for c in __bot.cookies.values():
            __driver.add_cookie(c)
        __driver.refresh()
    else:
        misc.print_wrn('man', 'I\'ll let you decide how sensible this is without being logged in ... ')
    return SUCCESS

def ls(*args):
    if len(args) == 2 and args[1] in ('?', 'help'):
        misc.print_dict('Help: "{} <opt.>"'.format(args[0]), HELP['ls, dir, list']['opts'])
        return SUCCESS

    for u in [d for d in os.listdir(params.TMP_PATH) if os.path.isdir(os.path.join(params.TMP_PATH, d))]:
        print(' {}{}{}{}{}{}'.format(cm.Style.BRIGHT, cm.Fore.LIGHTGREEN_EX, u, '' if len(args) == 2 and args[1] in ('u', 'users') else ':', 
                                     cm.Fore.RESET, cm.Style.RESET_ALL))
        ds = [d for d in os.listdir(os.path.join(params.TMP_PATH, u)) if os.path.isdir(os.path.join(params.TMP_PATH, u, d))]
        mgs = list(filter(lambda d: d.startswith('m'), ds))
        ogs = list(filter(lambda d: d.startswith('o'), ds))
        igs = list(filter(lambda d: d.startswith('i'), ds))
        if (len(args) < 2 or args[1] in ('m', 'media')) and len(mgs) > 0:
            print(' \tMedia: ')
            for mg in mgs:
                print(' \t  -> Grab: %s' % datetime.datetime.fromtimestamp(float(mg[1:])).isoformat())
        if (len(args) < 2 or args[1] in ('o', 'followers')) and len(ogs) > 0:
            print(' \tFollowers: ')
            for og in ogs:
                print(' \t  -> Grab: %s' % datetime.datetime.fromtimestamp(float(og[1:])).isoformat())
        if (len(args) < 2 or args[1] in ('i', 'following')) and len(igs) > 0:
            print(' \tFollowing: ')
            for ig in igs:
                print(' \t  -> Grab: %s' % datetime.datetime.fromtimestamp(float(ig[1:])).isoformat())
    return SUCCESS

def he(*args):
    misc.print_dict('Help', { k: v['desc'] for k, v in HELP.items() })
    return SUCCESS

def handle(com, debug=False):
    try:
        for k in COMS.keys():
            if com[0] in k:
                return COMS[k](*com)
        if com[0] == '':
            return SUCCESS
        misc.print_err('d4v1d', 'Unknown command: "{}"'.format(com[0]))
        return UNKNOWN
    except Exception as e:
        if debug:
            misc.print_err(str(e.__class__.__name__), str(e))
            traceback.print_exc()
        return FAILURE

# -- GLOBALS ----------------------------------------------------------------------------------------------------------------------------------------------- #

COMS = {
    ('clear','cls',): clear,
    ('exit','quit','bye','close',): bye,
    ('login',): login, 
    ('logout',): logout,
    ('show','display','sh','disp',): show,
    ('get','dump',): get,
    ('man','manual',): man,
    ('ls','dir','list',): ls,
    ('?','help','he',): he, 
}
HELP = {
    'clear, cls': {
        'desc': 'Clear the terminal',
    },
    'exit, quit, bye, close': {
        'desc': 'Close the terminal',
    },
    'login': {
        'desc': 'Log into an Instagram account',
        'opts': {
            'r, renew': 'Force a re-login',
            '?, help': 'Display this help',
        },
    },
    'logout': {
        'desc': 'Log out of your Instagram account',
    },
    'show, display, sh, disp': {
        'desc': 'Show information about an attribute',
        'opts': {
            'u, user': 'Show info about the current user',
            'h, headers': 'Show the current headers',
            'a, user-agent': 'Show the current User-Agent',
            'c, cookies': 'Shows all cookies in-use',
            '?, help': 'Display this help',
        },
    },
    'get, dump': {
        'desc': 'Retrieve Instagram information',
        'opts': {
            'v, overview': 'Get a compact overview of a user\'s account',
            'o, followers': 'Get a list of all people that a certain user follows',
            'i, following': 'Get a list of all people that follow a certain user',
            'm, media': 'Download all the media a certain user has uploaded',
            '?, help': 'Display this help',
        },
    },
    'man, manual': {
        'desc': 'Open a browser window with the current configuration',
    },
    'ls, dir, list': {
        'desc': 'List all downloads',
        'opts': {
            'm, media': 'List all downloaded media',
            'u, users': 'List all scraped users',
            'o, followers': 'List all scraped followers',
            'i, following': 'List all scraped following',
            '?, help': 'Display this help',
        },
    },
    '?, help, he': {
        'desc': 'Display help',
    },
}
CLOSING = -2
FAILURE = -1
UNKNOWN =  0
SUCCESS =  1

__bot = None
__driver = None