import os
from time import sleep
from selenium import webdriver
import lib.misc

def login():
    try:
        driver = webdriver.Firefox()
        driver.get('https://www.instagram.com/accounts/login')
        curl = driver.current_url
        while driver.current_url == curl:
            input(' Are you done? [PRESS ENTER] ')
            # sleep(1)
        cookies = driver.get_cookies()
        driver.quit()
        return { c['name']: c for c in list(map(conv_cookie, cookies)) }
    except Exception:
        lib.misc.print_wrn('Login', 'Unable to retrieve cookies ... ')
        return { }

def conv_cookie(c):
    allowed = [ 
        'version', 
        'name', 
        'value', 
        'port', 
        'port_specified', 
        'domain', 
        'domain_specified', 
        'domain_initial_dot', 
        'path', 
        'path_specified', 
        'secure', 
        'expires', 
        'discard', 
        'comment', 
        'comment_url', 
        'rest', 
        'rfc2109', 
    ]
    return { k: v for k, v in c.items() if k in allowed}

if __name__ == '__main__':
    cookies = login()
    print(cookies)