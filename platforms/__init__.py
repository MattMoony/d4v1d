"""
The plugin point for social-media platform
speficic implementations
"""

import pkgutil
import importlib
from types import ModuleType
from typing import *

PLATFORMS: Dict[str, ModuleType] = {
    'instagram': importlib.import_module('platforms.instagram'),
    'twitter': importlib.import_module('platforms.twitter'),
    **{
        name: importlib.import_module(name)
        for finder, name, ispkg in pkgutil.iter_modules()
        if name.startswith("d4v1d_p_")
    },
}