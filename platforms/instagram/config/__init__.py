"""
Contains configuration specific to the Instagram platform.
"""

import os
import json
import config
from log import log
# unusual, but I was getting weird import
# behaviour otherwise ...
from config import *
from .dbtype import InstagramDBType
from typing import *

class InstagramConfig(object):
    """
    Configuration class for Instagram.
    """

    ddir: str
    """The directory where Instagram data should be stored"""
    cdir: str
    """The directory where Instagram configuration files should be stored"""
    db_type: InstagramDBType
    """The type of database to use"""
    headers: Dict[str, str]
    """The headers to use for requests"""
    user_agents: List[str]
    """The user agents to use for requests"""
    __dont_save: bool = False
    """Set, if the config shouldn't be saved - e.g. if it was corrupted"""

    def __init__(self, ddir: str, cdir: str,  db_type: InstagramDBType, headers: Dict[str, str], user_agents: List[str]):
        """
        Creates a new InstagramConfig object

        Args:
            ddir (str): The directory where Instagram data should be stored
            cdir (str): The directory where Instagram configuration files should be stored
            db_type (InstagramDBType): The type of database to use
            headers (Dict[str, str]): The headers to use for requests
            user_agents (List[str]): The user agents to use for requests
        """
        self.ddir = ddir
        self.cdir = cdir
        self.db_type = db_type
        self.headers = headers
        self.user_agents = user_agents

    def __del__(self) -> None:
        """
        Do cleanup, like saving the config, once instagram
        is unloaded
        """
        if not self.__dont_save:
            with open(os.path.join(self.cdir, 'conf.json'), 'w') as f:
                json.dump(self.dumpj(), f)

    def dumpj(self) -> Dict[str, Any]:
        """
        Returns a dictionary representation of this object
        """
        return {
            'db_type': self.db_type.name,
            'headers': self.headers,
            'user_agents': self.user_agents
        }

    @classmethod
    def loadj(cls, data: Dict[str, Any]) -> "InstagramConfig":
        """
        Creates a new InstagramConfig object from a dictionary

        Args:
            data (Dict[str, Any]): The dictionary to load from
        """
        c: InstagramConfig
        cdir: str = os.path.join(config.PCONFIG.conf_dir, 'instagram')

        try:
            _c: Optional[InstagramConfig] = None
            # check if the db type actually exists
            if data['db_type'] not in InstagramDBType._member_names_:
                _c = cls.default(dont_save=True)
                log.error(f'Invalid database type used in your instagram config ("{data["db_type"]}") - using default option "{_c.db_type.name}" for now ...')
                log.error(f'To fix this error, choose an appropriate db type in "{os.path.join(cdir, "conf.json")}", i.e. one of: {", ".join(chr(0x22) + t.name + chr(0x22) for t in InstagramDBType)}')
                data['db_type'] = _c.db_type.name

            # try loading the config optimistically
            c = cls(
                os.path.join(config.PCONFIG.data_dir, 'instagram'),
                cdir,
                InstagramDBType[data['db_type']],
                data['headers'],
                data['user_agents']
            )

            # cleanup after *borked* db type
            if _c:
                print('not  saving ....')
                c.__dont_save = True
                del _c
        # should the config file be corrupted, we'll use the default one
        except KeyError:
            log.error(f'Instagram config file is corrupted - using default config ...')
            log.error(f'If you want to reset your config, delete {os.path.join(cdir, "conf.json")}')
            c = cls.default(dont_save=True)
        return c

    @classmethod
    def default(cls, dont_save: bool = False) -> "InstagramConfig":
        """
        Creates a new InstagramConfig object with default values

        Args:
            dont_save (bool): Set, if the config shouldn't be saved - e.g. if it was corrupted
        """
        c: InstagramConfig = cls(
            os.path.join(config.PCONFIG.data_dir, 'instagram'),
            os.path.join(config.PCONFIG.conf_dir, 'instagram'),
            InstagramDBType.SQLITE,
            dict(),
            [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0',
            ]
        )
        c.__dont_save = dont_save
        return c
