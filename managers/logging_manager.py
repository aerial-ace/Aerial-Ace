import logging
from logging.handlers import TimedRotatingFileHandler

def setup_logging():

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    file_handler = TimedRotatingFileHandler("logs/aerial-ace.log", when="midnight", interval=1, backupCount=7)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    formatter.datefmt = '%Y-%m-%d %H:%M:%S'
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)