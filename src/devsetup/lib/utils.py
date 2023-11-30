import contextlib
import logging
import os
import pty
import subprocess
import sys
from typing import Callable

from devsetup.config import CONFIG

logger = logging.getLogger(__name__)

@contextlib.contextmanager
def catch_print_and_exit():
    """
    Catches any exceptions thrown by the function, prints them, and exits with the return code
    """
    # todo: make this a context manager so the syntax is
    # with catch_print_and_exit():
    #     do_stuff()
    # instead of
    # catch_print_and_exit(lambda: do_stuff)
    try:
        yield
    except Exception as e:
        if CONFIG.get("debug", False):
            logger.exception(e)
        else:
            logger.error(e)
        if hasattr(e, "exit_code"):
            exit(e.exit_code)
        else:
            exit(1)

def run_command_and_stream_output_lines(
    command: list[str], 
    printer: Callable, 
    env: dict[str, str],
    *args, 
    **kwargs
):
    printer(f"ISPTY = {os.isatty(sys.stdout.fileno())}")
    master, slave = pty.openpty()  # Open a new pseudo-terminal
    subprocess.run
    process = subprocess.Popen(
        command,
        stdout=slave,
        stderr=slave,
        stdin=subprocess.PIPE,
        env=env,
    )

    os.close(slave)  # Close the slave descriptor, we don't need it
    stdout = []
    buffer = ""
    while True:
        try:
            buffer = buffer + os.read(master, 1024).decode()

        except OSError:  # Raised when the process ends
            break

        if not buffer:  # End of file
            break

        # add only whole lines to output
        # last index of \n
        end = buffer.rfind("\n")
        output, buffer = (
            (buffer[0:end], buffer[end + 1 : len(buffer)])
            if "\n" in buffer
            else ("", buffer)
        )
        for line in output.strip().splitlines():
            printer(line, *args, **kwargs)  # Log the output
            stdout.append(line)
    if buffer:
        printer(buffer, *args, **kwargs)
        stdout.append(buffer)

    os.close(master)
    process.wait()

    return subprocess.CompletedProcess(
        args=command,
        returncode=process.returncode,
        stdout="\n".join(stdout),
        stderr="",
    )
