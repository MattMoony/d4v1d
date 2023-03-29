"""
Grants d4v1d access to Tellonym.
"""

import json
import os

from d4v1d.log import log
from d4v1d.platforms.tellonym.config import TellonymConfig

from d4v1d import config
from d4v1d.platforms.tellonym.tellonym import Tellonym
from d4v1d.platforms.platform import Platform

def init() -> Platform:
    """
    Initialize everything - i.e. setup the TellonymConfig and
    initialize and return a new instance of Tellonym

    Returns:
        Platform: Tellonym platform interface
    """
    conf: TellonymConfig
    # create config directory if it doesn't exist
    cdir: str = os.path.join(config.PCONFIG.conf_dir, 'tellonym')
    if not os.path.isdir(cdir):
        os.mkdir(cdir)
    # create default config file if it doesn't exist
    if not os.path.isfile(os.path.join(cdir, 'conf.json')):
        conf = TellonymConfig.default()
        with open(os.path.join(cdir, 'conf.json'), 'w', encoding='utf8') as f:
            json.dump(conf.dumpj(), f)
    # load config file
    else:
        with open(os.path.join(cdir, 'conf.json'), 'r', encoding='utf8') as f:
            try:
                conf = TellonymConfig.loadj(json.load(f))
            except json.JSONDecodeError:
                log.error('Tellonym config file is corrupted - using default config ...')
                log.error('If you want to reset your config, delete "%s"', os.path.join(cdir, "conf.json"))
                conf = TellonymConfig.default(dont_save=True)
    # add config to global config
    config.PCONFIG._tellonym = conf  # pylint: disable=protected-access
    # create data directory if it doesn't exist
    if not os.path.isdir(conf.ddir):
        os.mkdir(conf.ddir)
    # initialize platform handler
    if os.path.isfile(os.path.join(conf.cdir, 'tellonym.json')):
        log.debug('Loading Tellonym data from "%s" ...', os.path.join(conf.cdir, "tellonym.json"))
        with open(os.path.join(conf.cdir, 'tellonym.json'), 'r', encoding='utf8') as f:
            try:
                return Tellonym.loadj(json.load(f))
            except json.JSONDecodeError:
                log.error('Tellonym data file is corrupted - using default data ...')
                log.error('If you want to reset your data, delete "%s"', os.path.join(conf.cdir, "tellonym.json"))
    return Tellonym()
