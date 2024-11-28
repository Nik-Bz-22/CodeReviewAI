import logging
from logging.handlers import RotatingFileHandler

from app.config import LOGS_DIR
import sys


def init_logging() -> logging.Logger:
    logger = logging.getLogger("core")
    if logger.hasHandlers():
        return logger
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "[%(asctime)s.%(msecs)03d] "
        "[PROCESS %(process)d %(processName)s] "
        "[THREAD %(thread)d %(threadName)s] "
        "%(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = RotatingFileHandler(
        filename=LOGS_DIR / "app.log",
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    httpx_logger = logging.getLogger("httpx")
    httpx_logger.setLevel(logging.WARNING)
    return logger

logger = init_logging()