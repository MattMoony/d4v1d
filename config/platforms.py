"""
Allows for platform-specific configuration
options.
"""

import os
from enum import Enum
from typing import *

class BaseOrigin(Enum):
    """
    Enum for the origin of the base path
    """
    ENV = 1
    """The base path is specified in the environment"""
    CONF = 2
    """The base path is specified in the config file"""
    DEFAULT = 3
    """The base path is the default one"""

class PlatformsConfig(object):
    """
    Contains some configuration options for
    platforms.
    """

    base_dir: str
    """
    The directory containing all platform-related content (base path) 
    - nothing should be stored in here directly
    """
    base_origin: BaseOrigin
    """The origin of the base path"""
    data_dir: str
    """The directory where data of all platforms should be stored"""
    __data_dir: str
    """Unparsed version of data_dir"""
    conf_dir: str
    """The directory where platforms can store configuration files"""
    __conf_dir: str
    """Unparsed version of conf_dir"""

    def __init__(self, base_dir: str, base_origin: BaseOrigin, data_dir: str, conf_dir: str):
        """
        Creates a new PlatformsConfig object
        """
        self.__dict__['base_dir'] = base_dir
        self.__dict__['base_origin'] = base_origin
        self.data_dir = data_dir
        self.conf_dir = conf_dir

    def dumpj(self) -> Dict[str, str]:
        """
        Returns a dictionary representation of this object
        """
        dump: Dict[str, str] = {
            'data_dir': self.data_dir,
            'conf_dir': self.conf_dir
        }
        if self.base_origin == BaseOrigin.CONF:
            dump['base_dir'] = self.base_dir
        return dump

    def __setattr__(self, k: str, v: Any) -> None:
        if k in ('data_dir', 'conf_dir',):
            self.__dict__[f'__{k}'] = v
            self.__dict__[k] = v.replace('$D4V1D_DIR', self.base_dir)
        elif k == 'base_dir':
            self.__dict__[k] = v
            self.__dict__['base_origin'] = BaseOrigin.CONF
            self.data_dir = self.__data_dir
            self.conf_dir = self.__conf_dir
        elif k.startswith('_'):
            # platform-specific options should always be
            # prefixed with an underscore
            self.__dict__[k] = v

    @classmethod
    def loadj(cls, j: Dict[str, str]) -> "PlatformsConfig":
        """
        Creates a new PlatformsConfig object from a dictionary
        """
        base_dir: str
        base_origin: BaseOrigin
        if 'base_dir' in j.keys():
            base_dir = j['base_dir']
            base_origin = BaseOrigin.CONF
        elif os.getenv('D4V1D_DIR'):
            base_dir = os.getenv('D4V1D_DIR')
            base_origin = BaseOrigin.ENV
        else:
            base_dir = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), '_')
            base_origin = BaseOrigin.DEFAULT
        return PlatformsConfig(base_dir, base_origin, j['data_dir'], j['conf_dir'])
    