"""
This module contains the commands that can be run from the command line.
"""

import logging

from devsetup.config import CONFIG, write_config
from devsetup.tap import get_tap

logger = logging.getLogger(__name__)


def get_tap_cmd():
    """Prints the current tap (according to the config)"""
    # use print so nothing else gets printed since this is used elsewhere
    print(get_tap())


def set_tap_cmd(tap: str):
    """Sets the tap in the config and saves it"""
    CONFIG["tap"] = tap
    logging.info("tap set to %s", tap)
    write_config()
