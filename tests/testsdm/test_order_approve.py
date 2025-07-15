# this page contains all the test cases for the samplePage
import pytest

from rich.traceback import install

from pages.digital_marketplace.checkout_page import CheckoutPage
from pages.digital_marketplace.home_page import HomePage
from pages.digital_marketplace.login_page import LoginPage
from pages.digital_marketplace.main_navigation_menu import MainNavigationMenu
from pages.digital_marketplace.pending_approval_orders import PendingApprovalOrders
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
    s_page.perform_login(
        user_name=TestResourcesDM.order_approver_PIN,
        pass_word=TestResourcesDM.order_approver_pass
    )


def test_two(resource):
    print("Test Two")
    r_page = HomePage(resource)
    r_page.goto_order_list()


def test_three(resource):
    print("Test Three")
    p_page = PendingApprovalOrders(resource)
    p_page.goto_pending_approval_orders_list()
    p_page.check_pending_approval()
    p_page.uncheck_pending_approval()
    p_page.search_order_input(
        order_reference_number=TestResourcesDM.search_order_reference_number
    )
    p_page.check_pending_approval()
    p_page.multiselect_approve()

# def test_four(resource):
#     print("Test Four")
#     p_page = PendingApprovalOrders(resource)
#     p_page.check_pending_approval()
