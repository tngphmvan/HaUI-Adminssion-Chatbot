"""
Set up logger with colorlog
"""
import logging

import colorlog


def setup_logger(name: str)-> logging.Logger:
    """
    Set up logger with colorlog
    Args:
        name (str): name of the logger
    Returns:
        setup_logger: logger with colorlog
    """
    log_format = "%(log_color)s[%(levelname)s]%(reset)s %(asctime)s - %(message)s"
    log_colors = {
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    }

    formatter = colorlog.ColoredFormatter(log_format, log_colors=log_colors)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG) # Set the default logging level for this logger
    logger.addHandler(handler)

    return logger