import logging
import colorlog

"""
Logging part

"""


def logger():
    # Create a logger with a name of your choosing
    logger = logging.getLogger("my_logger")

    # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    logger.setLevel(logging.DEBUG)

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

    # Add the handler to the logger
    logger.addHandler(console_handler)
    console_handler.setFormatter(formatter)
    return logger