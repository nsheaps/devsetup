import logging

from devsetup.brew.tap import TapNotSetError
from devsetup.brew.tap import get_tap as _get_tap
from devsetup.config import CONFIG, write_config
from devsetup.lib.errors import DEVSETUP_TAP_NOT_SET

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
    write_config()
    logger.info("tap set to %s", tap)
