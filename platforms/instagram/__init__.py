"""
Grants d4v1d access to Instagram.
"""

import os
import config
from .instagram import Instagram
from platforms.platform import Platform

def init() -> Platform:
    # extend PLATFORMS config with instagram-specific options
    if '.instagram' not in config.PLATFORMS.keys():
        config.PLATFORMS['.instagram'] = {
            'dir': os.path.join(config.PLATFORMS['data_dir'], 'instagram'),
        }
    # check if the data directory for instagram exists
    if not os.path.isdir(config.PLATFORMS['.instagram']['dir']):
        os.makedirs(config.PLATFORMS['.instagram']['dir'])
    return Instagram()
