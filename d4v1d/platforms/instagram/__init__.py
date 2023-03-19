"""
Grants d4v1d access to Instagram.
"""

import json
import os

from d4v1d.log import log
from d4v1d.platforms.instagram.config import InstagramConfig
# needs to be imported afterwards, as apparently
# the other import above would override it... :o
from d4v1d import config
from d4v1d.platforms.instagram.instagram import Instagram
from d4v1d.platforms.platform import Platform

def init() -> Platform:
    """
    Initialize everything - i.e. setup the InstagramConfig and
    initialize and return a new instance of Instagram

    Returns:
        Platform: Instagram platform interface
    """
    conf: InstagramConfig
    # create config directory if it doesn't exist
    cdir: str = os.path.join(config.PCONFIG.conf_dir, 'instagram')
    if not os.path.isdir(cdir):
        os.mkdir(cdir)
    # create default config file if it doesn't exist
    if not os.path.isfile(os.path.join(cdir, 'conf.json')):
        conf = InstagramConfig.default()
        with open(os.path.join(cdir, 'conf.json'), 'w', encoding='utf8') as f:
            json.dump(conf.dumpj(), f)
    # load config file
    else:
        with open(os.path.join(cdir, 'conf.json'), 'r', encoding='utf8') as f:
            try:
                conf = InstagramConfig.loadj(json.load(f))
            except json.JSONDecodeError:
                log.error('Instagram config file is corrupted - using default config ...')
                log.error('If you want to reset your config, delete "%s"', os.path.join(cdir, "conf.json"))
                conf = InstagramConfig.default(dont_save=True)
    # add config to global config
    config.PCONFIG._instagram = conf
    # create data directory if it doesn't exist
    if not os.path.isdir(conf.ddir):
        os.mkdir(conf.ddir)
    # initialize platform handler
    if os.path.isfile(os.path.join(conf.cdir, 'instagram.json')):
        log.debug('Loading Instagram data from "%s" ...', os.path.join(conf.cdir, "instagram.json"))
        with open(os.path.join(conf.cdir, 'instagram.json'), 'r', encoding='utf8') as f:
            try:
                return Instagram.loadj(json.load(f))
            except json.JSONDecodeError:
                log.error('Instagram data file is corrupted - using default data ...')
                log.error('If you want to reset your data, delete "%s"', os.path.join(conf.cdir, "instagram.json"))
    return Instagram()
