import os


class Config:

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    DATA_FOLDER = os.path.join(
        BASE_DIR,
        "data"
    )

    LOG_FOLDER = os.path.join(
        BASE_DIR,
        "logs"
    )

    DATA_FILE = os.path.join(
        DATA_FOLDER,
        "students.json"
    )

    LOG_FILE = os.path.join(
        LOG_FOLDER,
        "system.log"
    )

    SECRET_KEY = "student-information-system-secret-key"

    DEBUG = True