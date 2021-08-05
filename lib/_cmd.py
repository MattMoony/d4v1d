import os, argparse, traceback, datetime, time, json, webbrowser, shutil
from lib import misc, bot, api, params
from selenium import webdriver
import colorama as cm
import subprocess as sp
cm.init()

# -- UTILS ----------------------------------------------------------------------------------------------------------------------------------------------- #

class ArgumentParser(argparse.ArgumentParser):
    def error(self, msg):
        print(' %s' % msg)
        raise argparse.ArgumentError()

def __cleanup():
    if __driver:
        __driver.quit()

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
    elif args[1] in ('?', 'help'):
        misc.print_dict('Help: "{} <opt.>"'.format(args[0]), HELP['get, dump']['opts'])
    else:
        if len(args) < 3:
            misc.print_err(args[0], 'Missing arguments "{} {} <user>"'.format(args[0], args[1]))
        elif args[1] in ('v', 'overview'):
            misc.print_dict('Overview: {}'.format(args[2]), { k.title().replace('_', ' '): v for k, v in api.get_user_overview(args[2], headers=__bot.headers if __bot else {}).items()})
        elif args[1] in ('o', 'followers'):
            if not __bot:
                misc.print_err(args[0], 'You need to be logged in!')
                return FAILURE
            fs = __bot.get_followers(args[2])
            if len(fs) == 0:
                misc.print_wrn(args[0], 'No followers found. Maybe the account is private?')
                return FAILURE
            print(' Downloaded {}{}{} followers.'.format(cm.Style.BRIGHT, len(fs), cm.Style.RESET_ALL))
        elif args[1] in ('i', 'following'):
            if not __bot:
                misc.print_err(args[0], 'You need to be logged in!')
                return FAILURE
            fs = __bot.get_following(args[2])
            if len(fs) == 0:
                misc.print_wrn(args[0], 'No following found. Maybe the account is private?')
                return FAILURE
            print(' Downloaded {}{}{} following-connections.'.format(cm.Style.BRIGHT, len(fs), cm.Style.RESET_ALL))
        elif args[1] in ('m', 'media'):
            api.get_media(args[2], None, __bot.session if __bot else None)
        else:
            if len(args) < 4:
                misc.print_err('get', 'Missing arguments "{} {} {} <user2>"'.format(*args))
            elif args[1] in ('p', 'path'):
                u1, u2 = args[2:]
                if not __bot:
                    misc.print_err(args[0], 'You need to be logged in!')
                    return FAILURE
                shp = __bot.shortest_path(u2, u1)
                print(shp[0][1] + ''.join([' {} '.format('->' if i[0] else '<-') + i[1] for i in shp[1:]]))
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
    uname = None
    if len(args) == 2 and args[1] in ('?', 'help'):
        misc.print_dict('Help: "{} <opt.>"'.format(args[0]), HELP['ls, dir, list']['opts'])
        return SUCCESS
    elif len(args) == 2 and args[1].startswith('-u'):
        uname = args[1][2:]
        d = os.path.join(params.TMP_PATH, uname)
        if not os.path.isdir(d):
            misc.print_err('ls', 'User hasn\'t been scraped yet!')
            return FAILURE

    for u in [d for d in os.listdir(params.TMP_PATH) if os.path.isdir(os.path.join(params.TMP_PATH, d))]:
        if uname and u != uname:
            continue
        print(' {}{}{}{}{}{}'.format(cm.Style.BRIGHT, cm.Fore.LIGHTGREEN_EX, u, '' if len(args) == 2 and args[1] in ('u', 'users') else ':', 
                                     cm.Fore.RESET, cm.Style.RESET_ALL))
        ds = [d for d in os.listdir(os.path.join(params.TMP_PATH, u)) if os.path.isdir(os.path.join(params.TMP_PATH, u, d))]
        mgs = list(filter(lambda d: d.startswith('m'), ds))
        ogs = list(filter(lambda d: d.startswith('o'), ds))
        igs = list(filter(lambda d: d.startswith('i'), ds))
        if (len(args) < 2 or uname or args[1] in ('m', 'media')) and len(mgs) > 0:
            print(' \tMedia: ')
            for mg in mgs:
                print(' \t  -> Grab: %s' % datetime.datetime.fromtimestamp(float(mg[1:])).isoformat())
        if (len(args) < 2 or uname or args[1] in ('o', 'followers')) and len(ogs) > 0:
            print(' \tFollowers: ')
            for og in ogs:
                print(' \t  -> Grab: %s' % datetime.datetime.fromtimestamp(float(og[1:])).isoformat())
        if (len(args) < 2 or uname or args[1] in ('i', 'following')) and len(igs) > 0:
            print(' \tFollowing: ')
            for ig in igs:
                print(' \t  -> Grab: %s' % datetime.datetime.fromtimestamp(float(ig[1:])).isoformat())
    return SUCCESS

def browse(*args):
    cfile = os.path.join(params.SRV_PATH, 'config/conf.json')
    if not os.path.isfile(cfile):
        misc.print_err(args[0], '"{}" doesn\'t exist!'.format(cfile))
        return FAILURE
    with open(cfile, 'r') as f:
        conf = json.load(f)
        try:
            print(' Listening on http://localhost:%d ... ' % conf['port'])
            webbrowser.open('http://localhost:{}'.format(conf['port']))
        except KeyError:
            misc.print_err(args[0], 'Error: Malformed configuration file!')
    return SUCCESS

def rm(*args):
    if len(args) < 2:
        misc.print_err(args[0], 'Missing arguments "{} <opt.>"'.format(args[0]))
        return FAILURE
    elif args[1] in ('?', 'help'):
        misc.print_dict('Help: "{} <opt.>"'.format(args[0]), HELP['rm, del, remove, delete']['opts'])
    elif args[1] in ('p', 'purge'):
        count = 0
        size = 0
        for u in args[2].split(',') if len(args) >= 3 else os.listdir(params.TMP_PATH):
            ud = os.path.join(params.TMP_PATH, u)
            if not os.path.isdir(ud):
                continue
            print(' Purging "{}{}{}": '.format(cm.Fore.LIGHTGREEN_EX, u, cm.Fore.RESET), end='')
            ds = os.listdir(ud)
            print(' Media', end='')
            mfs = list(filter(lambda d: d.startswith('m'), ds))
            mfs.sort()
            for m in mfs[:-1]:
                size += sum([os.path.getsize(os.path.join(ud, m, f)) for f in os.listdir(os.path.join(ud, m)) if os.path.isfile(os.path.join(ud, m, f))])
                count+=1
                shutil.rmtree(os.path.join(ud, m))
            print('✔️, Followers', end='')
            ofs = list(filter(lambda d: d.startswith('o'), ds))
            ofs.sort()
            first = 0
            for i, o in enumerate(ofs[::-1]):
                if os.path.isfile(os.path.join(ud, o, 'followers.json')):
                    first = len(ofs)-i-1
                    break
            for o in [*ofs[:first],*ofs[first+1:]]:
                size += sum([os.path.getsize(os.path.join(ud, o, f)) for f in os.listdir(os.path.join(ud, o)) if os.path.isfile(os.path.join(ud, o, f))])
                count+=1
                shutil.rmtree(os.path.join(ud, o))
            print('✔️, Following', end='')
            ifs = list(filter(lambda d: d.startswith('i'), ds))
            ifs.sort()
            first = 0
            for j, i in enumerate(ifs[::-1]):
                if os.path.isfile(os.path.join(ud, i, 'following.json')):
                    first = len(ifs)-j-1
                    break
            for i in [*ifs[:first],*ifs[first+1:]]:
                size += sum([os.path.getsize(os.path.join(ud, i, f)) for f in os.listdir(os.path.join(ud, i)) if os.path.isfile(os.path.join(ud, i, f))])
                count+=1
                shutil.rmtree(os.path.join(ud, i))
            print('✔️')
        print(' Deleted {}{}{} directories, freeing up {}{:,.3f}{} MiB of space!'.format(cm.Style.BRIGHT, count, cm.Style.RESET_ALL, cm.Style.BRIGHT, size/2**20, cm.Style.RESET_ALL))
    return SUCCESS

def he(*args):
    misc.print_dict('Help', { k: v['desc'] for k, v in HELP.items() })
    return SUCCESS

def handle(com, debug=False):
    try:
        for k in COMS.keys():
            if com[0] in k:
                rc = COMS[k](*com)
                if rc == CLOSING:
                    __cleanup()
                return rc
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
    ('br','browse',): browse,
    ('rm','del','remove','delete',): rm,
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
            'p, path': 'Get the shortest path from one user to another',
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
    'br, browse': {
        'desc': 'Browse the downloaded information in your browser',
    },
    'rm, del, remove, delete': {
        'desc': 'Delete local items',
        'opts': {
            'p, purge': 'Remove all deprecated directories',
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