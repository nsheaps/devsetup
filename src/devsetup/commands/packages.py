from devsetup.brew.tap import get_tap


def install(formula: str, **kwargs):
    tap = get_tap()

    # if formula has any slashes in it, throw an error
    if "/" in formula:
        raise ValueError(
            f"formula cannot contain slashes, must be installed from upstream tap (currently: {tap})"
        )
