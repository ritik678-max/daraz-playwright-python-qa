import os

from dotenv import load_dotenv

from utils.constants import (
    DEFAULT_BROWSER,
    DEFAULT_HEADLESS,
    DEFAULT_TIMEOUT as FALLBACK_TIMEOUT,
    DEFAULT_WORKERS
)


# --------------------------------
# Environment Selection
# --------------------------------

ENV = os.getenv(
    "TEST_ENV",
    "qa"
)

env_file = f".env.{ENV}"

load_dotenv(
    env_file,
    override=False
)


# --------------------------------
# Base URL
# --------------------------------

BASE_URL = os.getenv(
    "BASE_URL",
    "https://www.daraz.com.np/"
)


# --------------------------------
# Browser
# --------------------------------

BROWSER = os.getenv(
    "BROWSER",
    DEFAULT_BROWSER
)


# --------------------------------
# Headless Mode
# --------------------------------

HEADLESS = os.getenv(
    "HEADLESS",
    str(DEFAULT_HEADLESS)
).lower() == "true"


# --------------------------------
# Timeout
# --------------------------------

DEFAULT_TIMEOUT = int(
    os.getenv(
        "DEFAULT_TIMEOUT",
        str(FALLBACK_TIMEOUT)
    )
)


# --------------------------------
# Parallel Workers
# --------------------------------

WORKERS = int(
    os.getenv(
        "WORKERS",
        str(DEFAULT_WORKERS)
    )
)