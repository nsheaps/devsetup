import logging
from argparse import ArgumentParser

from devsetup.commands import get_tap_cmd, set_tap_cmd


def main():
    parser = ArgumentParser()

    # debug flag
    parser.add_argument("-d", "--debug", action="store_true", help="debug flag")

    # subcommands
    subparsers = parser.add_subparsers(title="Commands", dest="command")

    # get-tap
    subparsers.add_parser("get-tap")

    # set-tap <tap>
    set_tap_parser = subparsers.add_parser("set-tap")
    set_tap_parser.add_argument("tap", help="tap to set")

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
        from devsetup import config

        config.set_debug(True)

    if args.command == "get-tap":
        get_tap_cmd()
    elif args.command == "set-tap":
        set_tap_cmd(args.tap)


if __name__ == "__main__":
    main()
