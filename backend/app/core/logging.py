import logging
import os
from logging.handlers import RotatingFileHandler

from app.config.settings import settings


def setup_logging() -> None:
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)

    # Get the root logger
    logger = logging.getLogger()

    # Set log level
    logger.setLevel(settings.log_level.upper())

    # Remove existing handlers to avoid duplicate logs
    logger.handlers.clear()

    # Log format
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File handler (rotating log file)
    file_handler = RotatingFileHandler(
        settings.log_file,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    # Register handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)