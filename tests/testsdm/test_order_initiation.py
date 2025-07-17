# this page contains all the test cases for the samplePage
import pytest

from rich.traceback import install

from pages.digital_marketplace.checkout_page import CheckoutPage
from pages.digital_marketplace.home_page import HomePage
from pages.digital_marketplace.login_page import LoginPage
from pages.digital_marketplace.main_navigation_menu import MainNavigationMenu
from pages.digital_marketplace.shopping_cart import ShoppingCart
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
    # s_page.click_on_btn()

    s_page.perform_login(
        user_name=TestResourcesDM.test_username,
        pass_word=TestResourcesDM.test_userpass
    )


def test_two(resource):
    print("Test Two")
    r_page = HomePage(resource)
    r_page.click_shopping_cart()


# def test_three(resource):
#     print("Test Three")
#     l_page = MainNavigationMenu(resource)
#     l_page.exit_button.click()

def test_three(resource):
    print("Test Three")
    v_page = ShoppingCart(resource)
    v_page.select_vendor()


def test_four(resource):
    print("Test Four")
    c_page = CheckoutPage(resource)
    c_page.delivery_schedule_preparation(
        location=TestResourcesDM.test_location,
        user_pin=TestResourcesDM.test_receiving_person_pin
    )
    # c_page.fill_delivery_info(text=)
    # c_page.click_add_schedule_btn()


def test_five(resource):
    print("Test Five")
    c_page = CheckoutPage(resource)
    c_page.click_add_schedule_btn()
