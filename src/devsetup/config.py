import logging
import os

import yaml

from .errors import DEVSETUP_CONFIG_FOLDER_EXISTS_BUT_IS_NOT_A_DIRECTORY

logger = logging.getLogger(__name__)

CONFIG = {}

CONFIG_FOLDER = "~/.config/devsetup/"
CONFIG_FOLDER_EXPANDED = os.path.expanduser(CONFIG_FOLDER)

CONFIG_FILE = "config.yaml"
CONFIG_FILE_PATH = os.path.join(CONFIG_FOLDER, CONFIG_FILE)
CONFIG_FILE_PATH_EXPANDED = os.path.expanduser(CONFIG_FILE_PATH)


def load_config():
    CONFIG["debug"] = False

    # make sure ~/.config/devsetup/ exists
    if os.path.exists(CONFIG_FOLDER_EXPANDED):
        # if it's a directory:
        if os.path.isdir(CONFIG_FOLDER_EXPANDED):
            logger.debug("%s exists", CONFIG_FOLDER)
        else:
            logger.error(f"{CONFIG_FOLDER} exists but is not a directory")
            exit(DEVSETUP_CONFIG_FOLDER_EXISTS_BUT_IS_NOT_A_DIRECTORY)
    else:
        logger.info(f"{CONFIG_FOLDER} does not exist, making it")
        os.mkdir(CONFIG_FOLDER_EXPANDED)

    # make sure ~/.config/devsetup/config.yaml exists
    if os.path.exists(CONFIG_FILE_PATH_EXPANDED):
        logger.debug(f"{CONFIG_FILE_PATH} exists")
    else:
        logger.info(f"{CONFIG_FILE_PATH} does not exist, making it")
        with open(CONFIG_FILE_PATH_EXPANDED, "w") as f:
            # copy the template from ./templates/config.yaml
            source = os.path.join(
                os.path.dirname(__file__), "../../", "templates", CONFIG_FILE
            )
            with open(source, "r") as s:
                f.write(s.read())
        logger.info(f"wrote {CONFIG_FILE_PATH}")

    # actually load the file
    with open(CONFIG_FILE_PATH_EXPANDED, "r") as f:
        CONFIG.update(yaml.safe_load(f))


load_config()


def write_config():
    """Converts CONFIG to yaml and writes it to CONFIG_FILE_PATH"""
    with open(CONFIG_FILE_PATH_EXPANDED, "w") as f:
        f.write(yaml.dump(CONFIG))
    logger.info(f"wrote {CONFIG_FILE_PATH}")


def set_debug(debug: bool):
    CONFIG["debug"] = debug
