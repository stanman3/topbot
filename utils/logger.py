# utils/logger.py
"""Logging configuration and utilities"""

import logging
from ..config.settings import LOG_LEVEL, LOG_FORMAT

def setup_logger(name: str = None) -> logging.Logger:
    """Set up and configure logger"""
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format=LOG_FORMAT
    )
    return logging.getLogger(name)

def get_logger(name: str = None) -> logging.Logger:
    """Get a logger instance"""
    return logging.getLogger(name)
