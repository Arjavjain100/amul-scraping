"""
Amul Scraper Package

A modular application for monitoring Amul product availability.
"""

# Version info
__version__ = "1.0.0"
__author__ = "Your Name"

# Common imports that might be used across modules
from typing import Dict, List, Any, Tuple, Optional

# Make key functions available at package level
from .api import fetch_api_data
from .db import init_db, update_db_and_notify, get_current_stock_status
from .notification import send_notification
from .logger import setup_logger, default_logger

__all__ = [
    'fetch_api_data',
    'init_db',
    'update_db_and_notify',
    'get_current_stock_status',
    'send_notification',
    'setup_logger',
    'default_logger'
]
