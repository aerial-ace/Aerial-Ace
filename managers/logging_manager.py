import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler


def setup_logging():
    if not os.path.exists("logs/"):
        os.mkdir("logs/")

    root_logger = logging.getLogger("aerial-ace")
    root_logger.setLevel(logging.INFO)
    root_logger.propagate = False

    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    formatter.datefmt = "%Y-%m-%d %H:%M:%S"

    file_handler = TimedRotatingFileHandler("logs/aerial-ace.log", when="midnight", interval=1, backupCount=7)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    root_logger.info("=============================================")
    root_logger.info("Logger Ready!")


def get_logger(name=None):
    return logging.getLogger("aerial-ace")
