"""
Dummy code for how a platform should
be implemented
"""

from typing import *

from d4v1d.platforms.platform.platform import Platform


def init() -> Platform:
    """
    Initialize the platform and return it.

    Returns:
        Platform: The initialized platform.
    """
    return Platform('dummy', 'Dummy Platform.')
