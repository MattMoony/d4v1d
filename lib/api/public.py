"""
All wrappers for public API endpoints are declared here. (public endpoints --> don't need to be logged in)
"""

from lib import models
from lib.api import base, urls
from typing import Any, Dict
import time
import requests as req
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def get_user(uname: str, headers: Dict[str, str] = {}) -> models.User:
    """
    Get an Instagram user by their username.

    Parameters
    ----------
    uname : str
        The username.
    headers : Dict[str, str]
        Optional; the headers that should be used for the request.
        Default is {}.
    """
    base.pause()
    res = req.get(urls.UINFO.format(uname), headers=headers).json()['graphql']['user']
    return models.User(int(res['id']), res['username'], res['biography'], res['external_url'], res['full_name'], 
                       res['is_business_account'], res['is_private'], res['is_verified'], res['profile_pic_url_hd'], 
                       res['edge_followed_by']['count'], res['edge_follow']['count'], res)

def get_username_by_id(uid: int, headers: Dict[str, str] = {}) -> str:
    """
    Gets the username of an Instagram user by their user-id.

    Parameters
    ----------
    uid : int
        The user-id.
    headers : Dict[str, str]
        Optional; the headers that should be used for the request.
        Default is {}.
    """
    base.pause()
    return req.get(urls.IINFO.format(uid), headers=headers).json()['user']['username']

def get_csrftoken() -> str:
    """Will make a request to Instagram and return the generated csrf-token."""
    opts = Options()
    opts.headless = True
    driver = webdriver.Firefox(options=opts)
    driver.get('https://www.instagram.com/')
    time.sleep(2)
    driver.find_element_by_tag_name('body').click()
    time.sleep(2)
    print(driver.get_cookies())
    return list(filter(lambda c: c['name'] == 'csrftoken', driver.get_cookies()))[0]['value']