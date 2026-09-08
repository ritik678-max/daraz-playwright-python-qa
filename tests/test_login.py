from playwright.sync_api import Page, expect


def test_login_form(page: Page):

    # Open login
    page.get_by_text("Login", exact=True).click()

    # Email / Phone
    email = page.get_by_placeholder(
        "Please enter your Phone or Email"
    )

    # Password
    password = page.locator(
        "input[type='password']"
    )

    # Verify fields
    expect(email).to_be_visible()
    expect(password).to_be_visible()

    # Enter test data
    email.fill("test@example.com")
    password.fill("tester@12")

    # Verify entered values
    expect(email).to_have_value("test@example.com")