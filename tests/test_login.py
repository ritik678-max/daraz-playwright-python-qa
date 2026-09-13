from playwright.sync_api import Page, expect

from utils.config import BASE_URL


def test_login_form(page: Page):

    page.goto(
        BASE_URL,
        wait_until="domcontentloaded"
    )

    # Open login form
    login_button = page.get_by_text(
        "Login",
        exact=True
    )

    expect(
        login_button
    ).to_be_visible()

    login_button.click()

    # Email / phone field
    email_field = page.get_by_placeholder(
        "Please enter your Phone or Email"
    )

    # Password field
    password_field = page.get_by_placeholder(
        "Please enter your password"
    )

    # Login submit button
    submit_button = page.get_by_role(
        "button",
        name="LOGIN"
    )

    expect(
        email_field
    ).to_be_visible()

    expect(
        password_field
    ).to_be_visible()

    expect(
        submit_button
    ).to_be_visible()