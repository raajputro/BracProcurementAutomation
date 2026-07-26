import os
import sys

from playwright.sync_api import sync_playwright

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pages.test_login import ResetHubPage
# from rich.traceback import install
# install()


def test_reset_login():
    reset_page = ResetHubPage(page=None)

    link = reset_page.generate_reset_link(
        env="erpstaging",
        username="761",
    )
    
    print("Generated Link:" + link)
    
    assert isinstance(link, str) and link.startswith("http")