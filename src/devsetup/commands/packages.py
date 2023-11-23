import logging
import subprocess
from devsetup.brew.tap import get_tap
from devsetup.lib.errors import FORMULA_CONTAINS_SLASHES
from devsetup.lib.utils import catch_print_and_exit


logger = logging.getLogger(__name__)


class FormulaCantContainSlashesError(Exception):
    """Raised when the formula contains slashes"""

    exit_code = FORMULA_CONTAINS_SLASHES

    def __init__(self, formula: str, tap: str):
        super().__init__(
            f"formula ({formula}) cannot contain slashes, must be installed from upstream tap (currently: {tap})"
        )


def install(formula: str, **kwargs):
    tap = catch_print_and_exit(lambda: get_tap())

    # if formula has any slashes in it, throw an error
    if "/" in formula:
        raise FormulaCantContainSlashesError(formula, tap)

    # install the formula
    logger.info(f"installing {tap}/{formula}...")

    subprocess.run(["brew", "install", f"{tap}/{formula}"])
