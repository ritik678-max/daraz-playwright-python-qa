import json
import os

import allure
import pytest
from playwright.sync_api import sync_playwright

from pages.home_page import HomePage
from pages.search_page import SearchPage
from pages.product_page import ProductPage
from utils.logger import setup_logging, get_logger, get_log_file
from utils.config import (
    BASE_URL,
    BROWSER,
    HEADLESS,
    WORKERS,
    ENV
)


# --------------------------------
# Logging Setup
# --------------------------------

setup_logging()
logger = get_logger(__name__)


def get_worker_id():
    """
    Returns xdist worker ID such as:
    gw0, gw1, gw2

    Normal pytest execution returns:
    main
    """
    return os.getenv(
        "PYTEST_XDIST_WORKER",
        "main"
    )


# --------------------------------
# Browser Fixture
# --------------------------------

@pytest.fixture(scope="session")
def browser():

    browser_name = BROWSER.lower()
    headless_mode = HEADLESS

    worker_id = get_worker_id()

    logger.info(
        f"Worker: {worker_id} | "
        f"Browser: {browser_name} | "
        f"Headless: {headless_mode}"
    )

    with sync_playwright() as playwright:

        if browser_name == "chromium":

            browser = playwright.chromium.launch(
                headless=headless_mode
            )

        elif browser_name == "firefox":

            browser = playwright.firefox.launch(
                headless=headless_mode
            )

        elif browser_name == "webkit":

            browser = playwright.webkit.launch(
                headless=headless_mode
            )

        else:

            raise ValueError(
                f"Unsupported browser: "
                f"{browser_name}"
            )

        yield browser

        browser.close()


# --------------------------------
# Browser Context
# --------------------------------

@pytest.fixture
def context(browser):

    os.makedirs(
        "test-results",
        exist_ok=True
    )

    context = browser.new_context(
        record_video_dir="test-results/"
    )

    yield context

    context.close()


# --------------------------------
# Page Fixture + Failure Video
# --------------------------------

@pytest.fixture
def page(context, request):

    page = context.new_page()

    yield page

    report = getattr(
        request.node,
        "rep_call",
        None
    )

    if report and report.failed:

        video = page.video

        if video:

            try:

                video_path = video.path()

                logger.error(
                    f"Failure video saved: "
                    f"{video_path}"
                )

                allure.attach.file(
                    video_path,
                    name="Failure Video",
                    attachment_type="video/webm",
                    extension="webm"
                )

            except Exception as error:

                logger.error(
                    f"Could not attach video: "
                    f"{error}"
                )

    page.close()


# --------------------------------
# Page Object Fixtures
# --------------------------------

@pytest.fixture
def home_page(page):
    return HomePage(page)


@pytest.fixture
def search_page(page):
    return SearchPage(page)


@pytest.fixture
def product_page(page):
    return ProductPage(page)


# --------------------------------
# Playwright Trace
# --------------------------------

@pytest.fixture(autouse=True)
def trace_test(page, request):

    os.makedirs(
        "traces",
        exist_ok=True
    )

    worker_id = get_worker_id()

    page.context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True
    )

    yield

    report = getattr(
        request.node,
        "rep_call",
        None
    )

    if report and report.failed:

        trace_path = (
            f"traces/"
            f"{worker_id}_"
            f"{request.node.name}.zip"
        )

        page.context.tracing.stop(
            path=trace_path
        )

        logger.error(
            f"Failure trace saved: "
            f"{trace_path}"
        )

        allure.attach.file(
            trace_path,
            name="Playwright Trace",
            attachment_type="application/zip",
            extension="zip"
        )

    else:

        page.context.tracing.stop()


# --------------------------------
# Attach Worker Log to Allure
# --------------------------------

@pytest.fixture(autouse=True)
def attach_log_to_allure(request):

    yield

    log_path = get_log_file()

    if os.path.exists(log_path):

        allure.attach.file(
            log_path,
            name=(
                f"Automation Log - "
                f"{os.path.basename(log_path)}"
            ),
            attachment_type="text/plain",
            extension="log"
        )


# --------------------------------
# Pytest Report
# Screenshot
# PASS / FAIL / SKIP Logging
# --------------------------------

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(
    item,
    call
):

    outcome = yield
    report = outcome.get_result()

    setattr(
        item,
        f"rep_{report.when}",
        report
    )

    if report.when == "call":

        worker_id = get_worker_id()

        # -------------------------
        # PASSED
        # -------------------------

        if report.passed:

            logger.info(
                f"TEST PASSED: "
                f"{item.name}"
            )

        # -------------------------
        # FAILED
        # -------------------------

        elif report.failed:

            logger.error(
                f"TEST FAILED: "
                f"{item.name}"
            )

            page = item.funcargs.get(
                "page"
            )

            if page:

                os.makedirs(
                    "screenshots",
                    exist_ok=True
                )

                screenshot_path = (
                    f"screenshots/"
                    f"{worker_id}_"
                    f"{item.name}.png"
                )

                try:

                    page.screenshot(
                        path=screenshot_path,
                        full_page=True
                    )

                    logger.error(
                        f"Failure screenshot saved: "
                        f"{screenshot_path}"
                    )

                    allure.attach.file(
                        screenshot_path,
                        name="Failure Screenshot",
                        attachment_type=
                        allure.attachment_type.PNG
                    )

                except Exception as error:

                    logger.error(
                        f"Could not capture "
                        f"screenshot: {error}"
                    )

        # -------------------------
        # SKIPPED
        # -------------------------

        elif report.skipped:

            logger.warning(
                f"TEST SKIPPED: "
                f"{item.name}"
            )


# --------------------------------
# Allure Executor Information
# --------------------------------

def create_allure_executor():

    os.makedirs(
        "allure-results",
        exist_ok=True
    )

    execution_type = os.getenv(
        "EXECUTION_TYPE",
        "local"
    ).lower()

    executor_data = {
        "name": "Daraz QA Automation",
        "type": "pytest",
        "buildName": (
            f"Daraz QA - {ENV}"
        ),
        "buildOrder": 1,
        "reportName": (
            "Daraz Playwright Test Report"
        ),
        "url": BASE_URL,
        "reportUrl": ""
    }

    if execution_type == "docker":

        executor_data["name"] = (
            "Docker"
        )

        executor_data["buildName"] = (
            f"Docker Test Run - {ENV}"
        )

    elif execution_type == "github":

        executor_data["name"] = (
            "GitHub Actions"
        )

        executor_data["buildName"] = (
            f"GitHub Actions - {ENV}"
        )

    executor_file = os.path.join(
        "allure-results",
        "executor.json"
    )

    with open(
        executor_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            executor_data,
            file,
            indent=4
        )

    logger.info(
        f"Allure executor file created: "
        f"{executor_file}"
    )


# --------------------------------
# Allure Environment Information
# --------------------------------

def pytest_sessionfinish(
    session,
    exitstatus
):

    # xdist workers should not
    # overwrite shared Allure files
    if os.getenv(
        "PYTEST_XDIST_WORKER"
    ):
        return

    os.makedirs(
        "allure-results",
        exist_ok=True
    )

    environment_file = os.path.join(
        "allure-results",
        "environment.properties"
    )

    with open(
        environment_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            f"Environment={ENV}\n"
        )

        file.write(
            f"Base_URL={BASE_URL}\n"
        )

        file.write(
            f"Browser={BROWSER}\n"
        )

        file.write(
            f"Headless={HEADLESS}\n"
        )

        file.write(
            f"Workers={WORKERS}\n"
        )

    logger.info(
        f"Allure environment file created: "
        f"{environment_file}"
    )

    # Create executor.json
    create_allure_executor()