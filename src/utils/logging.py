"""Logging configuration"""
import logging
from typing import Optional

LOG_FORMAT = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"
LOG_LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
}

def get_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """Get configured logger"""
    logger = logging.getLogger(f"phoenix.{name}")
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(handler)
    
    if level:
        logger.setLevel(LOG_LEVELS.get(level.lower(), logging.INFO))
    
    return logger
