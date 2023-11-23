"""
This module is used for interacting with homebrew taps (or the general concept of taps)
"""

from devsetup.config import CONFIG
from devsetup.lib.errors import DEVSETUP_TAP_NOT_SET


class TapNotSetError(Exception):
    """Raised when the tap is not set in the config"""

    exit_code = DEVSETUP_TAP_NOT_SET

    def __init__(self):
        super().__init__("tap is not set in config")


def get_tap():
    """Returns the current tap (according to the config)"""
    tap = CONFIG.get("tap", "")
    if tap is None or tap == "":
        raise TapNotSetError
    return tap
