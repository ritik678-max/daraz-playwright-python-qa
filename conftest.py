import os

import allure
import pytest
from playwright.sync_api import sync_playwright

from pages.home_page import HomePage
from pages.search_page import SearchPage
from pages.product_page import ProductPage
from utils.logger import get_logger
from utils.logger import setup_logging, get_logger


setup_logging()
logger = get_logger(__name__)


# --------------------------------
# Browser / Context / Page Fixtures
# --------------------------------

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=False
        )

        yield browser

        browser.close()


@pytest.fixture
def context(browser):
    os.makedirs("test-results", exist_ok=True)

    context = browser.new_context(
        record_video_dir="test-results/"
    )

    yield context

    context.close()


@pytest.fixture
def page(context, request):
    page = context.new_page()

    yield page

    report = getattr(request.node, "rep_call", None)

    if report and report.failed:
        video = page.video

        if video:
            try:
                video_path = video.path()

                logger.error(
                    f"Failure video saved: {video_path}"
                )

                allure.attach.file(
                    video_path,
                    name="Failure Video",
                    attachment_type="video/webm",
                    extension="webm"
                )

            except Exception as error:
                logger.error(
                    f"Could not attach video: {error}"
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

    os.makedirs("traces", exist_ok=True)

    page.context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True
    )

    yield

    report = getattr(request.node, "rep_call", None)

    if report and report.failed:
        trace_path = (
            f"traces/{request.node.name}.zip"
        )

        page.context.tracing.stop(
            path=trace_path
        )

        logger.error(
            f"Failure trace saved: {trace_path}"
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
# Attach Log to Allure
# --------------------------------

@pytest.fixture(autouse=True)
def attach_log_to_allure(request):
    yield

    log_path = "reports/automation.log"

    if os.path.exists(log_path):
        allure.attach.file(
            log_path,
            name="Automation Log",
            attachment_type="text/plain",
            extension="log"
        )


# --------------------------------
# Pytest Report + Screenshot + Logging
# --------------------------------

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    setattr(
        item,
        f"rep_{report.when}",
        report
    )

    if report.when == "call":

        # -------------------------
        # PASSED
        # -------------------------
        if report.passed:
            logger.info(
                f"TEST PASSED: {item.name}"
            )

        # -------------------------
        # FAILED
        # -------------------------
        elif report.failed:
            logger.error(
                f"TEST FAILED: {item.name}"
            )

            page = item.funcargs.get("page")

            if page:
                os.makedirs(
                    "screenshots",
                    exist_ok=True
                )

                screenshot_path = (
                    f"screenshots/"
                    f"{item.name}.png"
                )

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

        # -------------------------
        # SKIPPED
        # -------------------------
        elif report.skipped:
            logger.warning(
                f"TEST SKIPPED: {item.name}"
            )