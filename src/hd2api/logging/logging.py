import logging
from logging.handlers import RotatingFileHandler

hd2api_logger = logging.getLogger("hd2api_logger")


def setuphd2logging(log_dir="./logs/"):
    # Create a rotating file handler
    log_handler = RotatingFileHandler(
        f"{log_dir}hd2api_logger.log", maxBytes=5 * 1024 * 1024, backupCount=5
    )
    log_handler.setLevel(logging.WARNING)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    log_handler.setFormatter(formatter)

    log_handler2 = RotatingFileHandler(
        f"{log_dir}hd2api_loggerinfo.log", maxBytes=5 * 1024 * 1024, backupCount=5
    )
    log_handler2.setLevel(logging.INFO)
    # Create a logger and set its level
    hd2api_logger.setLevel(logging.INFO)

    log_handler2.setFormatter(formatter)

    # Set the handler to the logger
    hd2api_logger.addHandler(log_handler)

    hd2api_logger.addHandler(log_handler2)
