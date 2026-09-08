import re

from playwright.sync_api import expect


def test_daraz_homepage(page):
    expect(page).to_have_url(
        re.compile(r"https://www\.daraz\.com\.np/.*")
    )