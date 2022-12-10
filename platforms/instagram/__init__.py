"""
Grants d4v1d access to Instagram.
"""

import os
import json
import config
from log import log
from .instagram import Instagram
from .config import InstagramConfig
from platforms.platform import Platform

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
        with open(os.path.join(cdir, 'conf.json'), 'w') as f:
            json.dump(conf.dumpj(), f)
    # load config file
    else:
        with open(os.path.join(cdir, 'conf.json'), 'r') as f:
            try:
                conf = InstagramConfig.loadj(json.load(f))
            except json.JSONDecodeError:
                log.error(f'Instagram config file is corrupted - using default config ...')
                log.error(f'If you want to reset your config, delete "{os.path.join(cdir, "conf.json")}"')
                conf = InstagramConfig.default(dont_save=True)
    # add config to global config
    config.PCONFIG._instagram = conf
    # create data directory if it doesn't exist
    if not os.path.isdir(conf.ddir):
        os.mkdir(conf.ddir)
    # initialize platform handler
    return Instagram()
