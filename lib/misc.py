import shutil, random
import colorama as cm
cm.init()

FORE = list(vars(cm.Fore).values())

def rand_color():
    return FORE[random.randint(0, len(FORE)-1)]

def print_title(txt):
    ml = max([len(l) for l in txt.split('\n')])
    sz = shutil.get_terminal_size()
    for l in txt.split('\n'):
        print(' '*(int(sz.columns/2)-int(ml/2)), end='')
        print(''.join([rand_color()+c for c in l]))
    print(cm.Fore.RESET, end='')

def print_err(lbl, msg):
    print(cm.Fore.RED + cm.Style.BRIGHT + ' [-] ' + lbl + ': ' + cm.Style.RESET_ALL + cm.Fore.LIGHTRED_EX + msg + cm.Fore.RESET)

def print_wrn(lbl, msg):
    print(cm.Fore.YELLOW + cm.Style.BRIGHT + ' [!] ' + lbl + ': ' + cm.Style.RESET_ALL + cm.Fore.LIGHTYELLOW_EX + msg + cm.Fore.RESET)

def prompt(bot=None, lbl='d4v1d'):
    if bot:
        print('{}{}{}{}@'.format(cm.Fore.LIGHTMAGENTA_EX, cm.Style.BRIGHT, bot.user['username'], cm.Fore.WHITE), end='')
    return input('{}{}{}{} $ {}{}'.format(cm.Fore.LIGHTCYAN_EX, cm.Style.BRIGHT, lbl, cm.Fore.LIGHTBLUE_EX, cm.Fore.RESET, cm.Style.RESET_ALL)).strip().split(' ')

def print_dict(title, d):
    print(' {}{}{}{}{}'.format(cm.Style.BRIGHT, cm.Fore.LIGHTGREEN_EX, title, cm.Fore.RESET, cm.Style.RESET_ALL))
    for k, v in d.items():
        print(' \t{}{}: {}{}'.format(cm.Style.BRIGHT, k, cm.Style.RESET_ALL, v))

def printl(c='='):
    print(c*shutil.get_terminal_size().columns)