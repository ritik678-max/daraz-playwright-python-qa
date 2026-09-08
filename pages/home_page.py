from playwright.sync_api import Page

from utils.config import BASE_URL


class HomePage:

    def __init__(self, page: Page):
        self.page = page
        self.search_box = page.get_by_placeholder("Search in Daraz")

    def open(self):
        self.page.goto(BASE_URL)

    def search_product(self, product_name):
        self.search_box.fill(product_name)
        self.search_box.press("Enter")