import logging
import os
import sys
import io
from logging.handlers import RotatingFileHandler

try:
    import coloredlogs
    COLORED_LOGS = True
except ImportError:
    COLORED_LOGS = False

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_FILE_PATH = "logs/app.log"

def setup_logging():
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    file_handler = RotatingFileHandler(LOG_FILE_PATH, maxBytes=5 * 1024 * 1024, backupCount=3)
    file_handler.setFormatter(logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT))
    logger.addHandler(file_handler)

    if COLORED_LOGS:
        coloredlogs.install(
            level='INFO',
            logger=logger,
            fmt=LOG_FORMAT,
            datefmt=DATE_FORMAT
        )
    else:
        console_handler = logging.StreamHandler(io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8'))
        console_handler.setFormatter(logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT))
        logger.addHandler(console_handler)

    logger.info("Logging setup complete.")
    logger.debug("Debug logging is enabled.")
    logger.warning("Warning logging is enabled.")
    logger.error("Error logging is enabled.")
