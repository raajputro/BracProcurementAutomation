import sys, os, time
from playwright.sync_api import sync_playwright
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pages.test_login import ResetHubPage

# from rich.traceback import install
# install()

def test_reset_login():

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        reset_page = ResetHubPage(page)

        link = reset_page.generate_reset_link(
            env="erpstaging",
            username="761"
        )

        print("Generated Link:" + link)

    # reset_page.open_generated_link(link)