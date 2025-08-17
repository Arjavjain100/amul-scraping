"""
Centralized logging configuration for the Amul scraper application.
"""

import logging
import sys
from typing import Optional


def setup_logger(
    name: Optional[str] = None, level: int = logging.INFO
) -> logging.Logger:
    """
    Creates and configures a logger with consistent formatting.

    Args:
        name: Logger name (defaults to __name__ of calling module)
        level: Logging level (default: INFO)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name or __name__)

    # Avoid adding multiple handlers if logger already exists
    if logger.handlers:
        return logger

    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(handler)
    logger.setLevel(level)

    return logger


# Create a default logger for the application
default_logger = setup_logger("amul_scraper")
