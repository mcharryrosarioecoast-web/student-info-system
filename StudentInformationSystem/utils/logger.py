import logging
import os
from config import Config


def setup_logger():

    if not os.path.exists(Config.LOG_FOLDER):
        os.makedirs(Config.LOG_FOLDER)

    logger = logging.getLogger("StudentInformationSystem")

    logger.setLevel(logging.INFO)

    if not logger.handlers:

        file_handler = logging.FileHandler(
            Config.LOG_FILE,
            encoding="utf-8"
        )

        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )

        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    return logger