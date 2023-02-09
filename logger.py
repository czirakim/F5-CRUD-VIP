import logging
import colorlog

"""
Logging part

"""


def logger():

    # Create a handler to output the logs to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # color the message
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(levelname)s%(reset)s %(message)s",
        log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
        },
    )

    # Add format to handler
    console_handler.setFormatter(formatter)

    return console_handler
