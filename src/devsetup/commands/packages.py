import logging
import os
import pty
import subprocess
import sys
from devsetup.brew.tap import get_tap
from devsetup.lib.errors import FORMULA_CONTAINS_SLASHES
from devsetup.lib.utils import catch_print_and_exit, run_command_and_stream_output_lines


logger = logging.getLogger(__name__)
# handler = logging.StreamHandler()
# formatter = logging.Formatter("%(message)s")
# handler.setFormatter(formatter)
# logger.addHandler(handler)


class FormulaContainSlashesError(Exception):
    """Raised when the formula contains slashes"""

    exit_code = FORMULA_CONTAINS_SLASHES

    def __init__(self, formula: str, tap: str):
        super().__init__(
            f"formula ({formula}) cannot contain slashes, must be installed from upstream tap (currently: {tap})"
        )


def install(formula: str, **kwargs):
    with catch_print_and_exit():
        tap = get_tap()

    # if formula has any slashes in it, throw an error
    if "/" in formula:
        raise FormulaContainSlashesError(formula, tap)

    # install the formula
    logger.info(f"Installing {formula} from {tap}...")

    homebrew_env = os.environ.copy().update(
        {
            "HOMEBREW_NO_AUTO_UPDATE": "1",
        }
    )

    with catch_print_and_exit():
        run_command_and_stream_output_lines(
            ["brew", "install", f"{tap}/{formula}"],
            logger.info,
            homebrew_env,
        )

    logger.info(f"Installed {formula} from {tap}!")


def uninstall(formula: str, **kwargs):
    with catch_print_and_exit():
        tap = get_tap()

    # if formula has any slashes in it, throw an error
    if "/" in formula:
        raise FormulaContainSlashesError(formula, tap)

    # install the formula
    logger.info(f"Uninstalling {tap}/{formula}...")

    homebrew_env = os.environ.copy().update(
        {
            "HOMEBREW_NO_AUTO_UPDATE": "1",
        }
    )

    with catch_print_and_exit():
        run_command_and_stream_output_lines(
            ["brew", "uninstall", f"{tap}/{formula}"],
            logger.info,
            homebrew_env,
        )
    
    # uninstall the formula
    logger.info(f"Uninstalled {formula} from {tap}!")
