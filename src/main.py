import logging
from argparse import ArgumentParser

from devsetup.commands.tap import get_tap, set_tap


def main():
    parser = ArgumentParser()

    # debug flag
    parser.add_argument("-d", "--debug", action="store_true", help="debug flag")

    # subcommands
    subparsers = parser.add_subparsers(title="Commands", dest="command")

    # get-tap
    get_tap_parser = subparsers.add_parser("get-tap")
    get_tap_parser.set_defaults(func=get_tap)

    # set-tap <tap>
    set_tap_parser = subparsers.add_parser("set-tap")
    set_tap_parser.add_argument("tap", help="tap to set")
    set_tap_parser.set_defaults(func=set_tap)

    # install <formula>, also supports i <formula>
    install_parser = subparsers.add_parser("install", aliases=["i"])
    install_parser.add_argument("formula", help="formula to install")


    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
        from devsetup import config

        config.set_debug(True)

    # convert args from Namespace to dict
    kwargs = vars(args)

    args.func(**kwargs)

    # if args.command == "get-tap":
    #     get_tap()
    # elif args.command == "set-tap":
    #     set_tap(args.tap)


if __name__ == "__main__":
    main()
