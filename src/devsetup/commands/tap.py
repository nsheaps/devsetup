"""
This module contains the commands that can be run from the command line.
"""

import logging

from devsetup.config import CONFIG, write_config
from devsetup.brew.tap import get_tap as _get_tap, TapNotSetError
from devsetup.commands.errors import DEVSETUP_TAP_NOT_SET

logger = logging.getLogger(__name__)


def get_tap(**kwargs):
    """Prints the current tap (according to the config)"""
    # use print so nothing else gets printed since this is used elsewhere
    try:
        print(_get_tap())
    except TapNotSetError as e:
        logger.error(e)
        exit(DEVSETUP_TAP_NOT_SET)


def set_tap(tap: str, **kwargs):
    """Sets the tap in the config and saves it"""
    CONFIG["tap"] = tap
    logging.info("tap set to %s", tap)
    write_config()
