from playwright.sync_api import Page, expect

from utils.config import DEFAULT_TIMEOUT


class SearchPage:

    def __init__(self, page: Page):
        self.page = page

        self.product_links = page.locator("a[href*='/products/']")
        self.product_prices = page.locator("span.ooOxS")

    def wait_for_results(self):
        expect(
            self.product_links.first
        ).to_be_visible(timeout=DEFAULT_TIMEOUT)

    def get_product_count(self):
        return self.product_links.count()

    def get_first_product_name(self):
        first_product = self.product_links.first

        product_image = first_product.locator(
            "img[type='product']"
        ).last

        return product_image.get_attribute("alt")

    def get_first_product_price(self):
        return self.product_prices.first.inner_text()

    def open_first_product(self):
        first_product = self.product_links.first

        first_product.scroll_into_view_if_needed()

        try:
            first_product.click(
                timeout=5000
            )

        except Exception:
            first_product.click(
                force=True
            )