# ==============================================================================
# File: utils/logger.py
# Description: Centralized logging configuration for the application.
# ==============================================================================
import logging
import sys

def setup_logging(log_level: str = "INFO", log_dir: str = "logs"):
    """Setup comprehensive logging configuration."""
    from pathlib import Path
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)
    
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    if root_logger.hasHandlers():
        root_logger.handlers.clear()
        
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    file_handler = RotatingFileHandler(
        log_path / "jarvis.log", maxBytes=10*1024*1024, backupCount=5
    )
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # Suppress noisy third-party loggers
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("pygame").setLevel(logging.WARNING)
    
    logging.info("Logging system initialized.")
