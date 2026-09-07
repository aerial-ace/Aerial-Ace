import logging
import os
from logging.handlers import TimedRotatingFileHandler

main_logger = logging.getLogger("main")


def setup_logging():

    if not os.path.exists("logs/"):
        os.mkdir("logs/")

    main_logger.setLevel(logging.INFO)

    file_handler = TimedRotatingFileHandler("logs/aerial-ace.log", when="midnight", interval=1, backupCount=7)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    formatter.datefmt = "%Y-%m-%d %H:%M:%S"
    file_handler.setFormatter(formatter)

    main_logger.addHandler(file_handler)

