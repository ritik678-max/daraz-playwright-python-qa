from playwright.sync_api import Page, expect

from utils.config import BASE_URL, DEFAULT_TIMEOUT


class HomePage:

    def __init__(self, page: Page):
        self.page = page
        self.search_box = page.get_by_placeholder(
            "Search in Daraz"
        )

    def open(self):
        self.page.goto(
            BASE_URL,
            wait_until="domcontentloaded"
        )

    def search_product(self, product_name):

        expect(
            self.search_box
        ).to_be_visible(
            timeout=DEFAULT_TIMEOUT
        )

        expect(
            self.search_box
        ).to_be_enabled(
            timeout=DEFAULT_TIMEOUT
        )

        self.search_box.fill(
            product_name
        )

        self.search_box.press(
            "Enter"
        )