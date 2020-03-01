from time import sleep
from selenium import webdriver

def login():
    driver = webdriver.Firefox()
    driver.get('https://www.instagram.com/accounts/login')
    curl = driver.current_url
    while driver.current_url == curl:
        sleep(1)
    cookies = driver.get_cookies()
    driver.quit()
    return { c['name']: c for c in list(map(conv_cookie, cookies)) }

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