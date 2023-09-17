"""
This module is used for interacting with homebrew taps (or the general concept of taps)
"""

from devsetup.config import CONFIG


def get_tap():
    """Returns the current tap (according to the config)"""
    # use print so nothing else gets printed since this is used elsewhere
    return CONFIG["tap"]
