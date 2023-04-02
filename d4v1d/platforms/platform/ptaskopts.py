"""
Data class for storing some options for
platform-specific tasks.
"""

from dataclasses import dataclass
from typing import Optional

from d4v1d.platforms.platform.bot.group import Group


@dataclass
class PTaskOpts:
    """
    Data class for storing some options for
    platform-specific tasks.
    """

    refresh: bool = False
    """Whether to refresh the information, even if it has been cached locally."""
    cache_only: bool = False
    """Whether to only use cached information, and not refresh it."""
    group: Optional[Group] = None
    """Use this group for fetching the information."""
