import pytest
import allure
import playwright.sync_api

from utils.data_loader import load_search_data
from utils.logger import get_logger


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

    with allure.step("Open Daraz homepage"):
        home_page.open()
        logger.info("Daraz homepage opened")

    with allure.step(f"Search for product: {search_term}"):
        home_page.search_product(search_term)
        logger.info(f"Searching product: {search_term}")

    with allure.step("Wait for search results"):
        search_page.wait_for_results()
        logger.info("Search results loaded")

    with allure.step("Verify search result URL"):
        assert "daraz.com.np" in page.url
        assert "/catalog/" in page.url
        assert f"q={search_term}" in page.url

        logger.info(f"Search URL verified: {page.url}")

    with allure.step("Verify product count"):
        product_count = search_page.get_product_count()

        logger.info(
            f"Number of products found: {product_count}"
        )

        assert product_count > 0

    with allure.step("Get first product name"):
        product_name = search_page.get_first_product_name()

        logger.info(
            f"Product name: {product_name}"
        )

        assert product_name is not None
        assert product_name.strip() != ""

    with allure.step("Get first product price"):
        product_price = search_page.get_first_product_price()

        logger.info(
            f"Product price: {product_price}"
        )

        assert product_price.startswith("Rs.")

    with allure.step("Open first product"):
        search_page.open_first_product()

        logger.info(
            f"Opened first product: {product_name}"
        )

    with allure.step("Wait for product details"):
        product_page.wait_for_product_details()

        logger.info("Product details page loaded")

    with allure.step("Verify product details URL"):
        logger.info(
            f"Product URL: {page.url}"
        )

        assert "/products/" in page.url

    with allure.step("Verify product name"):
        details_product_name = product_page.get_product_title()

        logger.info(
            f"Details product name: {details_product_name}"
        )

        assert details_product_name.strip() != ""

        assert (
            product_name.strip()
            == details_product_name.strip()
        )

        logger.info(
            "Listing product name matches details page product name"
        )

    with allure.step("Verify product price"):
        details_product_price = product_page.get_product_price()

        logger.info(
            f"Details product price: {details_product_price}"
        )

        assert details_product_price.startswith("Rs.")

        assert (
            product_price.strip()
            == details_product_price.strip()
        )

        logger.info(
            "Listing price matches details page price"
        )