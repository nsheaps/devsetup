

import logging
from typing import Callable



def catch_print_and_exit(
    func: Callable,
    *args,
    **kwargs,
):
    """
    Catches any exceptions thrown by the function, prints them, and exits with the return code
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger = logging.getLogger(func.__module__)
        logger.error(e)
        if getattr(e, "exit_code"):
          exit(e.exit_code)
        else:
          exit(1) 
