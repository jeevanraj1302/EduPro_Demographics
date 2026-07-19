"""
EduPro Demographics — Logger Module
=====================================
Configures structured logging with loguru for the entire application.
Logs are written to both console (stderr) and a rotating file.
"""

import sys
from loguru import logger

from src.config import LOG_FILE, LOG_LEVEL, LOG_ROTATION, LOG_RETENTION


def setup_logger() -> None:
    """
    Initialize the application logger with console and file sinks.

    - Console: colored, human-readable format
    - File: structured format with rotation and retention policies
    """
    # Remove default handler
    logger.remove()

    # Console handler — colorized, concise
    logger.add(
        sys.stderr,
        level=LOG_LEVEL,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level:<8}</level> | "
            "<cyan>{module}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> — "
            "<level>{message}</level>"
        ),
        colorize=True,
        backtrace=True,
        diagnose=False,
    )

    # File handler — structured, rotating
    logger.add(
        str(LOG_FILE),
        level=LOG_LEVEL,
        format=(
            "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | "
            "{module}:{function}:{line} — {message}"
        ),
        rotation=LOG_ROTATION,
        retention=LOG_RETENTION,
        compression="zip",
        backtrace=True,
        diagnose=False,
        enqueue=True,  # Thread-safe
    )

    logger.info("Logger initialized successfully.")


# Auto-initialize on import
setup_logger()
