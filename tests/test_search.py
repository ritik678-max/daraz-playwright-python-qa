import os

import pytest
import allure
import playwright.sync_api

from utils.data_loader import load_search_data
from utils.logger import get_logger
from utils.config import ENV, BROWSER


logger = get_logger(__name__)


@allure.feature("Product Search")
@allure.story("Search and verify product details")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.search
@pytest.mark.parametrize(
    "search_term",
    load_search_data()
)
def test_product_search(
    page: playwright.sync_api.Page,
    home_page,
    search_page,
    product_page,
    search_term
):

    worker_id = os.getenv(
        "PYTEST_XDIST_WORKER",
        "main"
    )

    # --------------------------------
    # Dynamic Allure Labels
    # --------------------------------

    allure.dynamic.label(
        "environment",
        ENV
    )

    allure.dynamic.label(
        "browser",
        BROWSER
    )

    allure.dynamic.label(
        "worker",
        worker_id
    )

    allure.dynamic.parameter(
        "Search Term",
        search_term
    )

    allure.dynamic.title(
        f"Search and verify product - {search_term}"
    )

    # --------------------------------
    # Open Homepage
    # --------------------------------

    with allure.step(
        "Open Daraz homepage"
    ):
        home_page.open()

        logger.info(
            "Daraz homepage opened"
        )

    # --------------------------------
    # Search Product
    # --------------------------------

    with allure.step(
        f"Search for product: {search_term}"
    ):
        home_page.search_product(
            search_term
        )

        logger.info(
            f"Searching product: "
            f"{search_term}"
        )

    # --------------------------------
    # Wait For Search Results
    # --------------------------------

    with allure.step(
        "Wait for search results"
    ):
        search_page.wait_for_results()

        logger.info(
            "Search results loaded"
        )

    # --------------------------------
    # Verify Search URL
    # --------------------------------

    with allure.step(
        "Verify search result URL"
    ):

        assert "daraz.com.np" in page.url
        assert "/catalog/" in page.url
        assert f"q={search_term}" in page.url

        logger.info(
            f"Search URL verified: "
            f"{page.url}"
        )

    # --------------------------------
    # Verify Product Count
    # --------------------------------

    with allure.step(
        "Verify product count"
    ):

        product_count = (
            search_page.get_product_count()
        )

        logger.info(
            f"Number of products found: "
            f"{product_count}"
        )

        assert product_count > 0

        allure.dynamic.parameter(
            "Product Count",
            product_count
        )

    # --------------------------------
    # Get Product Name
    # --------------------------------

    with allure.step(
        "Get first product name"
    ):

        product_name = (
            search_page.get_first_product_name()
        )

        logger.info(
            f"Product name: "
            f"{product_name}"
        )

        assert product_name is not None
        assert product_name.strip() != ""

    # --------------------------------
    # Get Product Price
    # --------------------------------

    with allure.step(
        "Get first product price"
    ):

        product_price = (
            search_page.get_first_product_price()
        )

        logger.info(
            f"Product price: "
            f"{product_price}"
        )

        assert product_price.startswith(
            "Rs."
        )

    # --------------------------------
    # Open First Product
    # --------------------------------

    with allure.step(
        "Open first product"
    ):

        search_page.open_first_product()

        logger.info(
            f"Opened first product: "
            f"{product_name}"
        )

    # --------------------------------
    # Wait For Product Details
    # --------------------------------

    with allure.step(
        "Wait for product details"
    ):

        product_page.wait_for_product_details()

        logger.info(
            "Product details page loaded"
        )

    # --------------------------------
    # Verify Product URL
    # --------------------------------

    with allure.step(
        "Verify product details URL"
    ):

        logger.info(
            f"Product URL: "
            f"{page.url}"
        )

        assert "/products/" in page.url

    # --------------------------------
    # Verify Product Name
    # --------------------------------

    with allure.step(
        "Verify product name"
    ):

        details_product_name = (
            product_page.get_product_title()
        )

        logger.info(
            f"Details product name: "
            f"{details_product_name}"
        )

        assert (
            details_product_name.strip()
            != ""
        )

        assert (
            product_name.strip()
            == details_product_name.strip()
        )

        logger.info(
            "Listing product name "
            "matches details page product name"
        )

    # --------------------------------
    # Verify Product Price
    # --------------------------------

    with allure.step(
        "Verify product price"
    ):

        details_product_price = (
            product_page.get_product_price()
        )

        logger.info(
            f"Details product price: "
            f"{details_product_price}"
        )

        assert (
            details_product_price.startswith(
                "Rs."
            )
        )

        assert (
            product_price.strip()
            == details_product_price.strip()
        )

        logger.info(
            "Listing price matches "
            "details page price"
        )