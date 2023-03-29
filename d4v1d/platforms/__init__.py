"""
The plugin point for social-media platform
speficic implementations
"""

import importlib
import pkgutil
from types import ModuleType
from typing import Dict

PLATFORMS: Dict[str, ModuleType] = {
    'instagram': importlib.import_module('d4v1d.platforms.instagram'),
    'tellonym': importlib.import_module('d4v1d.platforms.tellonym'),
    # 'twitter': importlib.import_module('d4v1d.platforms.twitter'),
    **{
        name[len('d4v1d_p_'):]: importlib.import_module(name)
        for finder, name, ispkg in pkgutil.iter_modules()
        if name.startswith('d4v1d_p_')
    },
}
"""Dictionary of all platforms available for/usable by d4v1d."""
