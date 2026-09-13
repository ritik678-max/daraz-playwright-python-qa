import re

from playwright.sync_api import expect

from utils.config import BASE_URL


def test_daraz_homepage(page):

    page.goto(
        BASE_URL,
        wait_until="domcontentloaded"
    )

    expect(page).to_have_url(
        re.compile(
            r"https://www\.daraz\.com\.np/.*"
        )
    )