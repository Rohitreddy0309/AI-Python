"""
logger_setup.py

This module configures the logging for the application.
It sets the logging level to INFO and defines a standard log format
including timestamp, log level, and message.

The logger instance `logger` can be imported and used across the project
for consistent logging.
"""

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)
