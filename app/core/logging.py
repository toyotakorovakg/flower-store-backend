"""
Configure application logging.

This module sets up Python's logging module for structured output. By default
it logs to stdout in a JSON like format. Adjust the configuration here to
send logs to files or external services.
"""
import logging
import sys


def setup_logging() -> None:
    """Initialize logging for the application."""
    root_logger = logging.getLogger()
    # Avoid adding multiple handlers in case of reload.
    if root_logger.handlers:
        return

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        fmt='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S%z',
    )
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)


setup_logging()
