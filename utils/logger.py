# ==============================================================================
# File: utils/logger.py
# Description: Centralized logging configuration for the application.
# ==============================================================================
import logging
import sys

def setup_logging():
    """Configures the root logger for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('jarvis.log', mode='w'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    # Suppress overly verbose logs from third-party libraries
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("newsapi").setLevel(logging.WARNING)
