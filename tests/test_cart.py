import allure
import pytest

from utils.logger import get_logger


logger = get_logger(__name__)


@allure.feature("Cart")
@allure.story(
    "Guest user add-to-cart authentication"
)
@allure.severity(
    allure.severity_level.CRITICAL
)
@pytest.mark.regression
def test_guest_add_product_to_cart(
    home_page,
    search_page,
    product_page,
    cart_page
):

    search_term = "laptop"

    with allure.step(
        "Open Daraz homepage"
    ):

        home_page.open()

        logger.info(
            "Daraz homepage opened"
        )

    with allure.step(
        "Search for product"
    ):

        home_page.search_product(
            search_term
        )

        search_page.wait_for_results()

        logger.info(
            f"Search results loaded for: "
            f"{search_term}"
        )

    with allure.step(
        "Open first product"
    ):

        search_page.open_first_product()

        product_page.wait_for_product_details()

        logger.info(
            "Product details page loaded"
        )

    with allure.step(
        "Click Add to Cart"
    ):

        product_page.add_to_cart()

        logger.info(
            "Add to Cart clicked"
        )

    with allure.step(
        "Verify login prompt appears "
        "for guest user"
    ):

        cart_page.wait_for_login_prompt()

        assert (
            cart_page.is_login_prompt_visible()
        )

        logger.info(
            "Login prompt displayed "
            "for guest Add to Cart"
        )