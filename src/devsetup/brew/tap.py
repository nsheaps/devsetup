"""
This module is used for interacting with homebrew taps (or the general concept of taps)
"""

from devsetup.config import CONFIG

class TapNotSetError(Exception):
    """Raised when the tap is not set in the config"""
    pass

def get_tap():
    """Returns the current tap (according to the config)"""
    # use print so nothing else gets printed since this is used elsewhere
    tap = CONFIG.get("tap")
    if tap is None:
        raise TapNotSetError
    return tap
