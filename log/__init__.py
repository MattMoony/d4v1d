"""
Provides the logger for all kinds of warning / error
messages, etc.
"""

import config
import logging
from rich.logging import RichHandler

logging.basicConfig(
    level='NOTSET',
    format=config.LOG_FORMAT,
    datefmt='[%X]',
    handlers=[RichHandler(markup=True),],
)

log: logging.Logger = logging.getLogger('d4v1d')