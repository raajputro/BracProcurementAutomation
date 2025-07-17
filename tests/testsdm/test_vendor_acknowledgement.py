# this page contains all the test cases for the samplePage
import pytest

from rich.traceback import install

from pages.digital_marketplace.login_page import LoginPage
from pages.digital_marketplace.administration import Administration
from resources.DMResourceFile import TestResourcesDM
from utils.basic_actionsdm import BasicActionsDM
from playwright.sync_api import sync_playwright

install()


@pytest.fixture(scope='session', autouse=True)
def resource():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(args=["--start-maximized"], headless=False)
        context = browser.new_context(no_viewport=True)
        page = context.new_page()
        yield page
        page.close()
        context.close()
        browser.close()


def test_one(resource):
    print("Test One")
    s_page = LoginPage(resource)
    s_page.navigate_to_url(TestResourcesDM.test_url)

    s_page.perform_login(
        user_name=TestResourcesDM.test_vendor_username,
        pass_word=TestResourcesDM.test_userpass
    )
def test_two(resource):
    print("Test Two")
    a_page = Administration(resource)
    a_page.click_vendor_acknowledge(
        order_reference_no=TestResourcesDM.test_order_reference_no
    )
