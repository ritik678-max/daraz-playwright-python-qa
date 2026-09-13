from playwright.sync_api import Page, expect

from utils.config import DEFAULT_TIMEOUT


class CartPage:

    def __init__(self, page: Page):

        self.page = page

        self.email_field = page.get_by_placeholder(
            "Please enter your Phone or Email"
        )

        self.password_field = page.get_by_placeholder(
            "Please enter your password"
        )

        self.login_button = page.get_by_role(
            "button",
            name="LOGIN"
        )

    def wait_for_login_prompt(self):

        expect(
            self.email_field
        ).to_be_visible(
            timeout=DEFAULT_TIMEOUT
        )

        expect(
            self.password_field
        ).to_be_visible(
            timeout=DEFAULT_TIMEOUT
        )

        expect(
            self.login_button
        ).to_be_visible(
            timeout=DEFAULT_TIMEOUT
        )

    def is_login_prompt_visible(self):

        return (
            self.email_field.is_visible()
            and self.password_field.is_visible()
            and self.login_button.is_visible()
        )