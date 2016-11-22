import logging


LOGGER_NAME = "network_watchdog_logger"


def initialize_logger(file_path):
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(file_path)
    handler.setLevel(logging.INFO)
    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)
    return logger


def get_logger():
    return logging.getLogger(LOGGER_NAME)
