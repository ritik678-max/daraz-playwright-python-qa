import logging
import os


LOG_FILE = "reports/automation.log"


def setup_logging():
    os.makedirs("reports", exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler = logging.FileHandler(
        LOG_FILE,
        mode="w",
        encoding="utf-8"
    )

    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(formatter)

    logging.basicConfig(
        level=logging.INFO,
        handlers=[
            file_handler,
            console_handler
        ],
        force=True
    )


def get_logger(name):
    return logging.getLogger(name)