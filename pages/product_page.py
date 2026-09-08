from playwright.sync_api import Page, expect

from utils.config import DEFAULT_TIMEOUT


class ProductPage:

    def __init__(self, page: Page):
        self.page = page

        self.product_title = page.locator(
            "h1.pdp-mod-product-badge-title"
        )

        self.product_price = page.locator(
            "span.pdp-price"
        ).first

    def wait_for_product_details(self):
        expect(
            self.product_title
        ).to_be_visible(timeout=DEFAULT_TIMEOUT)

    def get_product_title(self):
        return self.product_title.inner_text()

    def get_product_price(self):
        return self.product_price.inner_text()