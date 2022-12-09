"""
Provides the logger for all kinds of warning / error
messages, etc.
"""

import config
import logging
from rich.logging import RichHandler

logging.basicConfig(
    level=config.LOG_LEVEL,
    format=config.LOG_FORMAT,
    datefmt=config.LOG_DATEFMT,
    handlers=[RichHandler(markup=True),],
)

log: logging.Logger = logging.getLogger(config.LOG_NAME)