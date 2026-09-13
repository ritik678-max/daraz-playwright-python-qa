import logging
import os


def get_log_file():

    worker_id = os.getenv(
        "PYTEST_XDIST_WORKER"
    )

    os.makedirs(
        "reports",
        exist_ok=True
    )

    if worker_id:
        return (
            f"reports/"
            f"automation_{worker_id}.log"
        )

    return "reports/automation.log"


def setup_logging():

    log_file = get_log_file()

    formatter = logging.Formatter(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    )

    file_handler = logging.FileHandler(
        log_file,
        mode="w",
        encoding="utf-8"
    )

    file_handler.setFormatter(
        formatter
    )

    console_handler = (
        logging.StreamHandler()
    )

    console_handler.setFormatter(
        formatter
    )

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